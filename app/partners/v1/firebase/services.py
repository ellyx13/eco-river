import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
from . import config







class FirebaseServices:
    def __init__(self, credentials_file_path, collection) -> None:
        self.credentials_file_path = credentials_file_path
        self.collection_name = collection
        # Use a service account.
        self.cred = credentials.Certificate(config.CREDENTIALS_FILE_PATH)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore_async.client()
        self.collection = self.db.collection(collection)
    
    async def add(self, data):
        _, doc = await self.collection.add(data)
        return doc

    async def get_by_id(self, document_id):
        doc_ref = self.collection.document(document_id)
        doc = await doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    
    
    
firebase_video_services = FirebaseServices(credentials_file_path=config.CREDENTIALS_FILE_PATH, collection='videos')