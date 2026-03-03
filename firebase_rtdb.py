import requests
import json
from datetime import datetime

# Firebase Realtime Database Configuration
FIREBASE_RTDB_URL = "https://ai-resume-builder-b5dfc-default-rtdb.firebaseio.com"
# Note: You'll need to get API key from Firebase Console > Project Settings > Service Accounts
# For now, we'll use the database without authentication (read the note at the end)

class FirebaseRTDB:
    def __init__(self):
        self.base_url = FIREBASE_RTDB_URL
        self.headers = {
            'Content-Type': 'application/json',
            # Add authentication header if you have API key:
            # 'Authorization': 'Bearer YOUR_API_KEY_HERE'
        }
    
    def get(self, path):
        """Get data from Firebase RTDB"""
        try:
            url = f"{self.base_url}/{path}.json"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting data from Firebase: {e}")
            return None
    
    def set(self, path, data):
        """Set data in Firebase RTDB"""
        try:
            url = f"{self.base_url}/{path}.json"
            response = requests.put(url, json=data, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error setting data in Firebase: {e}")
            return False
    
    def update(self, path, data):
        """Update data in Firebase RTDB"""
        try:
            url = f"{self.base_url}/{path}.json"
            response = requests.patch(url, json=data, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating data in Firebase: {e}")
            return False
    
    def delete(self, path):
        """Delete data from Firebase RTDB"""
        try:
            url = f"{self.base_url}/{path}.json"
            response = requests.delete(url, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error deleting data from Firebase: {e}")
            return False
    
    def get_all_resumes(self):
        """Get all resumes from Firebase"""
        try:
            resumes_data = self.get("resumes")
            if resumes_data:
                resumes = []
                for resume_id, resume_data in resumes_data.items():
                    if isinstance(resume_data, dict):
                        resume_data['id'] = resume_id
                        resumes.append(resume_data)
                # Sort by created_at (newest first)
                resumes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                return resumes
            return []
        except Exception as e:
            print(f"Error fetching all resumes: {e}")
            return []
    
    def get_resume(self, resume_id):
        """Get specific resume from Firebase"""
        try:
            resume_data = self.get(f"resumes/{resume_id}")
            if resume_data and isinstance(resume_data, dict):
                resume_data['id'] = resume_id
                return resume_data
            return None
        except Exception as e:
            print(f"Error fetching resume: {e}")
            return None
    
    def save_resume(self, resume_id, resume_data):
        """Save resume to Firebase"""
        return self.set(f"resumes/{resume_id}", resume_data)
    
    def update_resume(self, resume_id, resume_data):
        """Update resume in Firebase"""
        return self.update(f"resumes/{resume_id}", resume_data)
    
    def delete_resume(self, resume_id):
        """Delete resume from Firebase"""
        return self.delete(f"resumes/{resume_id}")

# Initialize Firebase RTDB connection
firebase_db = FirebaseRTDB()

# Test connection
def test_firebase_connection():
    """Test Firebase RTDB connection"""
    try:
        # Try to read from the database
        test_data = firebase_db.get("test")
        print("✅ Firebase RTDB Connection Test:")
        print(f"📡 Database URL: {FIREBASE_RTDB_URL}")
        print("🔗 Connection: Successful")
        return True
    except Exception as e:
        print("❌ Firebase RTDB Connection Test Failed:")
        print(f"📡 Database URL: {FIREBASE_RTDB_URL}")
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_firebase_connection()
