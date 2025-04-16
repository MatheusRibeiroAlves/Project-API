import firebase_admin
from firebase_admin import credentials, firestore
import logging

logging.basicConfig(level=logging.INFO)

def initialize_firebase():
    """Inicializa o SDK Admin do Firebase para Firestore."""
    try:
        cred = credentials.Certificate("credentials/processo-seletivo.json")
        firebase_admin.initialize_app(cred)
        logging.info("Firebase inicializado com sucesso.")
        return firestore.client()
    except Exception as e:
        logging.error(f"Erro ao inicializar o Firebase: {str(e)}")
        return None

db = initialize_firebase()

if db is None:
    logging.error("Falha ao inicializar o Firebase. O aplicativo não funcionará corretamente.")