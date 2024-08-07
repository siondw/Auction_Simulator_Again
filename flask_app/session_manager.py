# session_manager.py

# Define the global session_data dictionary
session_data = {}

def get_session_data():
    global session_data  # Declare it as global to ensure we access the correct variable
    print(f"Accessing session_data: {session_data}")
    return session_data
