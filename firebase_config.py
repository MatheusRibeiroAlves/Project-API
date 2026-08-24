import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from unittest.mock import MagicMock

logging.basicConfig(level=logging.INFO)


def initialize_firebase():
    if os.environ.get("TEST_ENVIRONMENT") == "true":
        return MagicMock()
    cred = credentials.Certificate("credentials/processo-seletivo.json")
    firebase_admin.initialize_app(cred)
    logging.info("Firebase inicializado com sucesso.")
    return firestore.client()


db = initialize_firebase()
