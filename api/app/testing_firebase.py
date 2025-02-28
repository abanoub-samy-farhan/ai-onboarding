import firebase_admin
import firebase_admin.firestore
import pyrebase

cred = firebase_admin.credentials.Certificate('/home/abanoubaziz/Documents/Study/Personal Projects/ai-onboarding/api/app/onboarding-ai-74ac7-firebase-adminsdk-fbsvc-28b4c5a64b.json')
firebase_admin.initialize_app(cred)

db = firebase_admin.firestore.client()

config = {
  "apiKey": "AIzaSyBIIXFQNzfLSYUKUE8zqWkALSIWAWXjXF4",
  "authDomain": "onboarding-ai-74ac7.firebaseapp.com",
  "projectId": "onboarding-ai-74ac7",
  "storageBucket": "onboarding-ai-74ac7.firebasestorage.app",
  "messagingSenderId": "506614552197",
  "appId": "1:506614552197:web:84d8a305aa3f7e27cbfbec",
  "measurementId": "G-25JT84C29J"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
