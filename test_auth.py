
from src.database import initialize_database
from src.auth import register_user, authenticate_user

initialize_database()

# Register a test employer.
try:
    user_id = register_user(
        full_name="Test Employer",
        email="employer_test@example.com",
        password="EmployerPassword123!",
        role="employer"
    )

    print("Employer registration successful. User ID:", user_id)

except ValueError as error:
    print("Registration:", error)

# Test employer login.
user = authenticate_user(
    "employer_test@example.com",
    "EmployerPassword123!"
)

if user:
    print("Employer login successful!")
    print("Name:", user["full_name"])
    print("Role:", user["role"])
else:
    print("Employer login failed!")
