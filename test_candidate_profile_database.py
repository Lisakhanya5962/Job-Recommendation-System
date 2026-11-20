
from uuid import uuid4

from src.database import (
    create_user,
    get_user_by_id,
    save_candidate_profile,
    get_candidate_profile,
    get_connection
)


def test_candidate_profile_database():

    test_email = f"database_test_{uuid4().hex[:8]}@example.com"
    user_id = None

    try:
        # Create a temporary candidate account.
        user_id = create_user(
            full_name="Database Test Candidate",
            email=test_email,
            password_hash="test-only-password-hash",
            role="candidate"
        )

        # Save a sample candidate profile.
        save_candidate_profile(
            user_id=user_id,
            phone="",
            location="South Africa",
            cv_filename="test_cv.pdf",
            cv_text="",
            skills=["Python", "Communication"],
            qualifications=["Diploma"],
            experience=[],
            fields_of_study=["Information Technology"],
            institutions=["Nelson Mandela University"]
        )

        # Retrieve the saved profile.
        profile = get_candidate_profile(user_id)

        assert profile is not None
        assert profile["skills"] == [
            "Python",
            "Communication"
        ]
        assert profile["qualifications"] == ["Diploma"]
        assert profile["experience"] == []
        assert profile["fields_of_study"] == [
            "Information Technology"
        ]
        assert profile["institutions"] == [
            "Nelson Mandela University"
        ]

        print("Candidate profile saved successfully!")
        print("All five profile categories retrieved correctly!")
        print("DATABASE PROFILE TEST PASSED!")

    finally:
        # Remove the temporary test account.
        if user_id is not None:
            connection = get_connection()

            try:
                connection.execute(
                    "DELETE FROM users WHERE id = ?",
                    (user_id,)
                )
                connection.commit()
            finally:
                connection.close()


if __name__ == "__main__":
    test_candidate_profile_database()
