import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    """Inicializa o SDK Admin do Firebase para Firestore."""
    cred = credentials.Certificate("credentials/processo-seletivo-63cf4-firebase-adminsdk-fbsvc-eccd860f0e.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firebase()