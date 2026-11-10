
# Import the library for reading large JSON files
import ijson

# Open the first sessions dataset
with open("sessions_0.json", "rb") as file:

    # Read only the first session
    sessions = ijson.items(file, "item")
    first_session = next(sessions, None)

    # Check if a session was found
    if first_session is not None:

        # Get device information from the session
        device_profile = first_session.get("device_profile", {})

        print("DEVICE PROFILE STRUCTURE")
        print("-" * 40)

        # Display the names and values of device fields
        for field, value in device_profile.items():
            print(f"{field}: {value}")

    else:
        print("No session found in the file.")
