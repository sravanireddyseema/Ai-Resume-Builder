import os
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase with your service account
def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Path to your service account key
            cred_path = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')
            
            # Initialize Firebase Admin SDK with Realtime Database
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'projectId': 'ai-resume-builder-b5dfc',
                'databaseURL': 'https://ai-resume-builder-b5dfc-default-rtdb.firebaseio.com/'
            })
        
        # Get Realtime Database reference
        database = db.reference()
        return database
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def get_database():
    """Get Firebase Realtime Database instance"""
    try:
        return db.reference()
    except Exception as e:
        print(f"Error getting database reference: {e}")
        return None

# Initialize database
database = initialize_firebase()
