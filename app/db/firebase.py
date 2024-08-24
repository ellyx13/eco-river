import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
from . import config

class FirebaseEngine:
    def __init__(self) -> None:
        # Use a service account.
        self.cred = credentials.Certificate(config.CREDENTIALS_FILE_PATH)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore_async.client()
    
    def set_collection(self, collection: str):
        return self.db.collection(collection)
    
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(FirebaseEngine, cls).__new__(cls)
        return cls.instance

firebase_engine = FirebaseEngine()