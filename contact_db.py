import datetime as dt
from pymongo import MongoClient
import certifi

# MongoDB connection string placeholder
atlas = '## MONGO DB CLUSTER'

# Class to handle writing contact information to a MongoDB database
class WriteContactDb():
    def __init__(self, name, email, subject, message):
        # Store the current date and contact details
        self.date = dt.datetime.now()  # Current date and time
        self.name = name  # Contact's name
        self.email = email  # Contact's email
        self.subject = subject  # Contact's subject of message
        self.message = message  # The message body
        self.db()  # Call the database function to insert the data
        print(f"DATE:{self.date}")  # Print the current timestamp

    def db(self):
        # Prepare a dictionary for the document to be inserted into MongoDB
        contact_query = {
            "date": self.date,
            "name": self.name,
            "email": self.email,
            "message": self.message
        }
        try:
            # Connect to MongoDB using the client and a secure CA certificate
            client = MongoClient(
                atlas,
                tlsCAFile=certifi.where())

            # Check connection to MongoDB
            client.admin.command('ping')
            print("Connected to MongoDB")

            # Access the specified database and collection
            db = client["YOUR DB"]
            collection = db["YOUR DB COLLECTION"]

            # Insert the contact document into the collection
            insert_doc = collection.insert_one(contact_query)
            print(f"Document inserted with id: {insert_doc.inserted_id}")  # Print the inserted document ID

        # Handle potential exceptions during the connection or insertion process
        except Exception as error:
            print(f"there was an error: {error}")

        # Ensure that the connection is closed after the operation
        finally:
            client.close()
            print("Connection closed")
