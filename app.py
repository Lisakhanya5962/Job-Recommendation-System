
import streamlit as st

from src.database import (
    initialize_database,
    save_candidate_profile,
    get_candidate_profile
)

from src.auth import register_user, authenticate_user

from src.cv_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from src.candidate_profile_extractor import (
    extract_candidate_profile
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()


# ==================================================
# CUSTOM DESIGN AND COLOURS
# ==================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F4F7FB;
    color: #243447;
}

/* Main content width */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Main headings */
h1, h2, h3 {
    color: #102A43 !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    color: #334E68;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #102A43;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: transparent;
    border-radius: 8px;
    padding: 5px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #0F766E !important;
    color: #000000 !important;
    border: none;
    border-radius: 9px;
    padding: 0.65rem 1rem;
    font-weight: 700;
    transition: 0.2s ease;
}

/* Ensure button labels remain black */
.stButton > button p,
.stFormSubmitButton > button p,
.stButton > button span,
.stFormSubmitButton > button span {
    color: #000000 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #D9A441 !important;
    color: #000000 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #115E59;
    color: white !important;
    border: none;
    transform: translateY(-1px);
}

/* Input fields */
.stTextInput input,
.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
    color: #243447;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #0F766E;
}

/* Select and upload areas */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 1px dashed #0F766E;
    border-radius: 12px;
    padding: 12px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0F766E;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(16, 42, 67, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #627D98 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #102A43 !important;
    font-weight: 700;
}

/* Cards */
.custom-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 15px;
    box-shadow: 0 3px 12px rgba(16, 42, 67, 0.04);
}

.hero {
    background: linear-gradient(120deg, #102A43, #0F766E);
    border-radius: 18px;
    padding: 40px 35px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white !important;
    font-size: 2.5rem;
}

.hero p {
    color: #E0F2F1 !important;
    font-size: 1.1rem;
}

.section-label {
    color: #0F766E;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.8rem;
}

.small-note {
    color: #627D98;
    font-size: 0.9rem;
}

.gold-line {
    height: 4px;
    width: 65px;
    background-color: #D9A441;
    border-radius: 5px;
    margin: 10px 0 20px 0;
}

/* Dividers */
hr {
    border-color: #E2E8F0;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Form containers */
[data-testid="stForm"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 22px;
}

/* Footer */
.footer {
    text-align: center;
    color: #829AB1;
    font-size: 0.85rem;
    padding: 25px 0 5px 0;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def logout():
    st.session_state.user = None
    st.session_state.page = "Home"
    st.rerun()


def extract_uploaded_cv(uploaded_file):

    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    raise ValueError("Please upload a PDF or DOCX file.")


def show_section_heading(title, description=None):

    st.markdown(f"## {title}")

    if description:
        st.caption(description)


def show_footer():

    st.markdown("""
    <div class="footer">
        AI Job Recommendation System · Connecting Skills to Opportunities
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# HOME PAGE
# ==================================================

def show_home():

    st.markdown("""
    <div class="hero">
        <div class="section-label" style="color:#F5D58A;">
            CAREER OPPORTUNITIES START HERE
        </div>
        <h1>Find the Right Job.<br>Build Your Future.</h1>
        <p>
            Discover career opportunities that match your skills,
            qualifications and experience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### A smarter way to connect talent with opportunity")

    st.write(
        "Our platform analyses candidate CVs and helps connect "
        "job seekers with suitable opportunities. Employers can "
        "also publish vacancies and discover potential candidates."
    )

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown("""
        <div class="custom-card">
            <div class="section-label">FOR JOB SEEKERS</div>
            <h3>👤 Find Your Next Opportunity</h3>
            <p>
                Build your candidate profile, upload your CV,
                discover matching vacancies and track your applications.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Candidate Login",
            use_container_width=True,
            key="home_candidate_login"
        ):
            st.session_state.page = "Candidate Login"
            st.rerun()

        if st.button(
            "Create Candidate Account",
            use_container_width=True,
            key="home_candidate_register"
        ):
            st.session_state.page = "Candidate Registration"
            st.rerun()

    with col2:

        st.markdown("""
        <div class="custom-card">
            <div class="section-label">FOR EMPLOYERS</div>
            <h3>🏢 Find the Right Talent</h3>
            <p>
                Create an employer account, publish vacancies
                and discover candidates whose profiles match your requirements.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Employer Login",
            use_container_width=True,
            key="home_employer_login"
        ):
            st.session_state.page = "Employer Login"
            st.rerun()

        if st.button(
            "Create Employer Account",
            use_container_width=True,
            key="home_employer_register"
        ):
            st.session_state.page = "Employer Registration"
            st.rerun()

    st.divider()

    st.markdown("### How it works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("#### 01 · Create an account")
        st.write("Register as a candidate or employer.")

    with step2:
        st.markdown("#### 02 · Build your profile")
        st.write("Upload a CV or publish a job advertisement.")

    with step3:
        st.markdown("#### 03 · Discover opportunities")
        st.write("Connect suitable candidates with job opportunities.")

    show_footer()


# ==================================================
# REGISTRATION
# ==================================================

def show_registration(role):

    st.markdown(f"## Create Your {role.title()} Account")

    st.caption(
        "Complete the details below to join the AI Job Recommendation System."
    )

    with st.form(f"{role}_registration_form"):

        full_name = st.text_input("Full Name")

        email = st.text_input("Email Address")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submitted:

            if not full_name.strip() or not email.strip():
                st.warning("Please complete your name and email address.")

            elif not password:
                st.warning("Please enter a password.")

            elif password != confirm_password:
                st.error("Passwords do not match.")

            else:

                try:

                    register_user(
                        full_name=full_name.strip(),
                        email=email.strip(),
                        password=password,
                        role=role
                    )

                    st.success("Your account has been created successfully!")

                    st.info("You can now return to the login page.")

                except ValueError as error:
                    st.error(str(error))

                except Exception:
                    st.error(
                        "Unable to create your account. "
                        "Please try again."
                    )

    if st.button("← Back to Home"):
        st.session_state.page = "Home"
        st.rerun()


# ==================================================
# LOGIN
# ==================================================

def show_login(role):

    st.markdown(f"## Welcome Back")

    st.caption(f"Sign in to your {role} account.")

    with st.form(f"{role}_login_form"):

        email = st.text_input("Email Address")

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )

        if submitted:

            if not email.strip() or not password:
                st.warning("Please enter your email and password.")

            else:

                user = authenticate_user(
                    email.strip(),
                    password
                )

                if user and user["role"] == role:

                    st.session_state.user = user

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error(
                        "Invalid email, password or account type."
                    )

    if st.button("← Back to Home"):
        st.session_state.page = "Home"
        st.rerun()


# ==================================================
# CANDIDATE CV UPLOAD
# ==================================================

def show_cv_upload(user):

    show_section_heading(
        "Upload Your CV",
        "Build your candidate profile by uploading your latest CV."
    )

    st.markdown("""
    <div class="custom-card">
        <h4>📄 Your CV helps us understand your profile</h4>
        <p>
            We analyse your document to identify your skills,
            qualifications, education and work experience.
        </p>
        <p class="small-note">
            Supported formats: PDF and DOCX.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("candidate_cv_upload_form"):

        uploaded_file = st.file_uploader(
            "Choose your CV document",
            type=["pdf", "docx"],
            help="Upload a PDF or DOCX document."
        )

        submitted = st.form_submit_button(
            "Upload and Analyse CV",
            use_container_width=True
        )

        if submitted:

            if uploaded_file is None:

                st.warning("Please select a CV before continuing.")

            else:

                try:

                    with st.spinner("Analysing your CV. Please wait..."):

                        cv_text = extract_uploaded_cv(uploaded_file)

                        if not cv_text.strip():

                            st.error(
                                "No readable text was found. "
                                "Your PDF may be scanned or image-based."
                            )
                            return

                        profile = extract_candidate_profile(cv_text)

                        # Do not store the raw CV text.
                        save_candidate_profile(
                            user_id=user["id"],
                            cv_filename=uploaded_file.name,
                            cv_text="",
                            skills=profile["skills"],
                            qualifications=profile["qualifications"],
                            experience=profile["experience"],
                            fields_of_study=profile["fields_of_study"],
                            institutions=profile["institutions"]
                        )

                    st.success(
                        "Your CV has been analysed and your profile saved!"
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Unable to process your CV: {error}"
                    )


# ==================================================
# CANDIDATE PROFILE
# ==================================================

def show_candidate_profile(user):

    show_section_heading(
        "Your Candidate Profile",
        "Review the information extracted from your CV."
    )

    profile = get_candidate_profile(user["id"])

    if not profile:

        st.info(
            "Your profile is not ready yet. "
            "Upload your CV to get started."
        )
        return

    st.markdown(f"""
    <div class="custom-card">
        <div class="section-label">CURRENT CV</div>
        <h4>📄 {profile['cv_filename'] or 'CV not available'}</h4>
        <p class="small-note">
            Your extracted profile information is displayed below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        with st.container(border=True):

            st.markdown("### 💡 Skills")

            if profile["skills"]:

                for skill in profile["skills"]:
                    st.write(f"• {skill}")

            else:
                st.info("No skills identified.")

        with st.container(border=True):

            st.markdown("### 🎓 Qualifications")

            if profile["qualifications"]:

                for qualification in profile["qualifications"]:
                    st.write(f"• {qualification}")

            else:
                st.info("No qualifications identified.")

    with col2:

        with st.container(border=True):

            st.markdown("### 📚 Fields of Study")

            if profile["fields_of_study"]:

                for field in profile["fields_of_study"]:
                    st.write(f"• {field}")

            else:
                st.info("No fields of study identified.")

        with st.container(border=True):

            st.markdown("### 🏫 Educational Institutions")

            if profile["institutions"]:

                for institution in profile["institutions"]:
                    st.write(f"• {institution}")

            else:
                st.info("No institutions identified.")

    st.markdown("### 💼 Work Experience")

    with st.container(border=True):

        if profile["experience"]:

            for index, item in enumerate(
                profile["experience"],
                start=1
            ):

                st.write(f"**{index}.** {item}")

        else:

            st.info(
                "No work experience was identified. "
                "You can still receive entry-level job recommendations."
            )


# ==================================================
# CANDIDATE DASHBOARD
# ==================================================

def candidate_dashboard(user):

    st.markdown("## Candidate Dashboard")

    st.write(f"Welcome back, **{user['full_name']}** 👋")

    st.caption(
        "Manage your CV, review your profile and discover job opportunities."
    )

    profile = get_candidate_profile(user["id"])

    if profile:

        cv_status = "Uploaded"
        skills_count = len(profile["skills"])
        experience_count = len(profile["experience"])

    else:

        cv_status = "Not uploaded"
        skills_count = 0
        experience_count = 0

    st.markdown("### Your Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "CV Status",
        cv_status
    )

    col2.metric(
        "Extracted Skills",
        skills_count
    )

    col3.metric(
        "Experience Entries",
        experience_count
    )

    col4.metric(
        "Applications",
        "0"
    )

    st.divider()

    show_cv_upload(user)

    st.divider()

    show_candidate_profile(user)

    st.divider()

    st.markdown("### 🎯 Job Recommendations")

    st.info(
        "Your personalised job recommendations will appear here "
        "once the recommendation engine is connected."
    )

    show_footer()


# ==================================================
# EMPLOYER DASHBOARD
# ==================================================

def employer_dashboard(user):

    st.markdown("## Employer Dashboard")

    st.write(f"Welcome back, **{user['full_name']}** 👋")

    st.caption(
        "Your workspace for managing vacancies and discovering talent."
    )

    st.markdown("### Employer Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Published Jobs", "0")
    col2.metric("Applications", "0")
    col3.metric("Shortlisted Candidates", "0")

    st.divider()

    st.markdown("### 🏢 Your Employer Workspace")

    st.markdown("""
    <div class="custom-card">
        <h4>Manage your recruitment activities</h4>
        <p>
            Your employer workspace will help you publish vacancies,
            receive applications and identify suitable candidates.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### 📋 Job Management")

        st.write("• Create company profile")
        st.write("• Publish job advertisements")
        st.write("• Upload PDF and DOCX job advertisements")

    with col2:

        st.markdown("#### 👥 Candidate Management")

        st.write("• View candidate applications")
        st.write("• Review candidate profiles")
        st.write("• Shortlist suitable candidates")

    st.info(
        "Employer job management and candidate review features "
        "will be implemented in the next development stages."
    )

    show_footer()


# ==================================================
# MAIN APPLICATION ROUTING
# ==================================================

def main():

    with st.sidebar:

        st.markdown("""
        <div style="text-align:center; padding:15px 0 25px 0;">
            <div style="font-size:42px;">💼</div>
            <h3 style="color:white !important; margin:0;">
                AI JobMatch
            </h3>
            <p style="color:#BCCCDC; font-size:12px;">
                Connecting Skills to Opportunities
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        if st.session_state.user is None:

            st.markdown("### Navigation")

            pages = [
                "Home",
                "Candidate Login",
                "Candidate Registration",
                "Employer Login",
                "Employer Registration"
            ]

            selected_page = st.radio(
                "Choose a page",
                pages,
                index=pages.index(st.session_state.page)
            )

            st.session_state.page = selected_page

        else:

            user = st.session_state.user

            st.markdown("### Account")

            st.write(f"**{user['full_name']}**")

            st.caption(
                f"Account type: {user['role'].title()}"
            )

            st.divider()

            if st.button(
                "🚪 Logout",
                use_container_width=True
            ):
                logout()

        st.divider()

        st.caption("AI Job Recommendation System")
        st.caption("Version 1.0")


    # APPLICATION CONTENT

    if st.session_state.user:

        user = st.session_state.user

        if user["role"] == "candidate":

            candidate_dashboard(user)

        elif user["role"] == "employer":

            employer_dashboard(user)

        else:

            st.error("Unknown account role.")

    else:

        page = st.session_state.page

        if page == "Home":
            show_home()

        elif page == "Candidate Registration":
            show_registration("candidate")

        elif page == "Employer Registration":
            show_registration("employer")

        elif page == "Candidate Login":
            show_login("candidate")

        elif page == "Employer Login":
            show_login("employer")


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":
    main()
