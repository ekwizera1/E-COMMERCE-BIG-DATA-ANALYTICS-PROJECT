
# Import MongoClient to connect Python to MongoDB
from pymongo import MongoClient

# Connect to the local MongoDB server
client = MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

try:
    # Send a ping command to test the connection
    client.admin.command("ping")

    # Display a message if the connection works
    print("SUCCESS: Python connected to MongoDB!")

except Exception as error:
    # Display the error if the connection fails
    print("ERROR: MongoDB connection failed.")
    print(error)

finally:
    # Close the connection
    client.close()
