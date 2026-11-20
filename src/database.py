
import sqlite3
import json
from pathlib import Path


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "jobs.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create tables and safely migrate existing databases."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                description TEXT,
                required_skills TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK(role IN ('candidate', 'employer', 'admin')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidate_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                phone TEXT,
                location TEXT,
                cv_filename TEXT,
                cv_text TEXT,
                skills TEXT DEFAULT '[]',
                qualifications TEXT DEFAULT '[]',
                experience TEXT DEFAULT '[]',
                fields_of_study TEXT DEFAULT '[]',
                institutions TEXT DEFAULT '[]',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        # Safely add new columns to existing candidate_profiles tables.
        existing_columns = {
            row["name"]
            for row in cursor.execute(
                "PRAGMA table_info(candidate_profiles)"
            ).fetchall()
        }

        if "fields_of_study" not in existing_columns:
            cursor.execute("""
                ALTER TABLE candidate_profiles
                ADD COLUMN fields_of_study TEXT DEFAULT '[]'
            """)

        if "institutions" not in existing_columns:
            cursor.execute("""
                ALTER TABLE candidate_profiles
                ADD COLUMN institutions TEXT DEFAULT '[]'
            """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employer_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                company_name TEXT NOT NULL,
                industry TEXT,
                company_location TEXT,
                website TEXT,
                description TEXT,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_owners (
                job_id INTEGER PRIMARY KEY,
                employer_id INTEGER NOT NULL,

                FOREIGN KEY (job_id)
                    REFERENCES jobs(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (employer_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                cover_letter TEXT,
                match_score REAL DEFAULT 0,
                status TEXT DEFAULT 'pending'
                    CHECK(status IN (
                        'pending',
                        'reviewing',
                        'shortlisted',
                        'rejected',
                        'accepted'
                    )),
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(candidate_id, job_id),

                FOREIGN KEY (candidate_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (job_id)
                    REFERENCES jobs(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

    finally:
        connection.close()


# --------------------------------------------------
# JOB FUNCTIONS
# --------------------------------------------------

def add_job(title, company, required_skills,
            location="", description=""):

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO jobs (
                title, company, location,
                description, required_skills
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            company,
            location,
            description,
            json.dumps(required_skills)
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_all_jobs():

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT * FROM jobs ORDER BY id DESC
        """).fetchall()

        jobs = []

        for row in rows:
            job = dict(row)
            job["required_skills"] = json.loads(
                job["required_skills"]
            )
            jobs.append(job)

        return jobs

    finally:
        connection.close()


def get_job_by_id(job_id):

    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,)
        ).fetchone()

        if row is None:
            return None

        job = dict(row)
        job["required_skills"] = json.loads(
            job["required_skills"]
        )

        return job

    finally:
        connection.close()


def update_job(job_id, title, company, required_skills,
               location="", description=""):

    connection = get_connection()

    try:
        cursor = connection.execute("""
            UPDATE jobs
            SET title = ?,
                company = ?,
                location = ?,
                description = ?,
                required_skills = ?
            WHERE id = ?
        """, (
            title,
            company,
            location,
            description,
            json.dumps(required_skills),
            job_id
        ))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


def delete_job(job_id):

    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM jobs WHERE id = ?",
            (job_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


# --------------------------------------------------
# USER FUNCTIONS
# --------------------------------------------------

def create_user(full_name, email, password_hash, role):

    if role not in ("candidate", "employer", "admin"):
        raise ValueError("Invalid user role.")

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO users (
                full_name, email, password_hash, role
            )
            VALUES (?, ?, ?, ?)
        """, (
            full_name.strip(),
            email.strip().lower(),
            password_hash,
            role
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_user_by_email(email):

    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),)
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


def get_user_by_id(user_id):

    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


# --------------------------------------------------
# CANDIDATE PROFILE FUNCTIONS
# --------------------------------------------------

def save_candidate_profile(
    user_id,
    phone="",
    location="",
    cv_filename="",
    cv_text="",
    skills=None,
    qualifications=None,
    experience=None,
    fields_of_study=None,
    institutions=None
):

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO candidate_profiles (
                user_id, phone, location, cv_filename,
                cv_text, skills, qualifications, experience,
                fields_of_study, institutions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                phone = excluded.phone,
                location = excluded.location,
                cv_filename = excluded.cv_filename,
                cv_text = excluded.cv_text,
                skills = excluded.skills,
                qualifications = excluded.qualifications,
                experience = excluded.experience,
                fields_of_study = excluded.fields_of_study,
                institutions = excluded.institutions,
                updated_at = CURRENT_TIMESTAMP
        """, (
            user_id,
            phone,
            location,
            cv_filename,
            cv_text,
            json.dumps(skills or []),
            json.dumps(qualifications or []),
            json.dumps(experience or []),
            json.dumps(fields_of_study or []),
            json.dumps(institutions or [])
        ))

        connection.commit()
        return True

    finally:
        connection.close()


def get_candidate_profile(user_id):

    connection = get_connection()

    try:
        row = connection.execute("""
            SELECT * FROM candidate_profiles
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        if not row:
            return None

        profile = dict(row)

        for field in (
            "skills",
            "qualifications",
            "experience",
            "fields_of_study",
            "institutions"
        ):
            profile[field] = json.loads(
                profile.get(field) or "[]"
            )

        return profile

    finally:
        connection.close()


# --------------------------------------------------
# EMPLOYER PROFILE FUNCTIONS
# --------------------------------------------------

def save_employer_profile(
    user_id,
    company_name,
    industry="",
    company_location="",
    website="",
    description=""
):

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO employer_profiles (
                user_id, company_name, industry,
                company_location, website, description
            )
            VALUES (?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                company_name = excluded.company_name,
                industry = excluded.industry,
                company_location = excluded.company_location,
                website = excluded.website,
                description = excluded.description
        """, (
            user_id,
            company_name,
            industry,
            company_location,
            website,
            description
        ))

        connection.commit()
        return True

    finally:
        connection.close()


def get_employer_profile(user_id):

    connection = get_connection()

    try:
        row = connection.execute("""
            SELECT * FROM employer_profiles
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()


# --------------------------------------------------
# JOB OWNERSHIP
# --------------------------------------------------

def assign_job_to_employer(job_id, employer_id):

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO job_owners (job_id, employer_id)
            VALUES (?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                employer_id = excluded.employer_id
        """, (job_id, employer_id))

        connection.commit()
        return True

    finally:
        connection.close()


def get_employer_jobs(employer_id):

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT jobs.*
            FROM jobs
            JOIN job_owners
                ON jobs.id = job_owners.job_id
            WHERE job_owners.employer_id = ?
            ORDER BY jobs.id DESC
        """, (employer_id,)).fetchall()

        jobs = []

        for row in rows:
            job = dict(row)
            job["required_skills"] = json.loads(
                job["required_skills"]
            )
            jobs.append(job)

        return jobs

    finally:
        connection.close()


# --------------------------------------------------
# APPLICATION FUNCTIONS
# --------------------------------------------------

def apply_for_job(candidate_id, job_id, cover_letter="",
                  match_score=0):

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO applications (
                candidate_id, job_id,
                cover_letter, match_score
            )
            VALUES (?, ?, ?, ?)
        """, (
            candidate_id,
            job_id,
            cover_letter,
            match_score
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_candidate_applications(candidate_id):

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT
                applications.*,
                jobs.title,
                jobs.company,
                jobs.location
            FROM applications
            JOIN jobs ON jobs.id = applications.job_id
            WHERE applications.candidate_id = ?
            ORDER BY applications.applied_at DESC
        """, (candidate_id,)).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_job_applications(job_id):

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT
                applications.*,
                users.full_name,
                users.email
            FROM applications
            JOIN users ON users.id = applications.candidate_id
            WHERE applications.job_id = ?
            ORDER BY applications.applied_at DESC
        """, (job_id,)).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def update_application_status(application_id, status):

    allowed_statuses = (
        "pending",
        "reviewing",
        "shortlisted",
        "rejected",
        "accepted"
    )

    if status not in allowed_statuses:
        raise ValueError("Invalid application status.")

    connection = get_connection()

    try:
        cursor = connection.execute("""
            UPDATE applications
            SET status = ?
            WHERE id = ?
        """, (status, application_id))

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()
