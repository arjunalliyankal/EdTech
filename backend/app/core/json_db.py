import json
import os
import asyncio
from typing import Any, Dict, List, Optional
from bson import ObjectId

class JsonCollection:
    def __init__(self, db, collection_name: str):
        self.db = db
        self.name = collection_name

    def _get_data(self) -> List[Dict]:
        return self.db.data.get(self.name, [])

    def _save_data(self, data: List[Dict]):
        self.db.data[self.name] = data
        self.db._save()

    async def find_one(self, filter: Dict, sort: Optional[List] = None) -> Optional[Dict]:
        data = self._get_data()
        for item in data:
            match = True
            for k, v in filter.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                return item
        return None

    async def insert_one(self, document: Dict) -> Any:
        data = self._get_data()
        if "_id" not in document:
            document["_id"] = str(ObjectId())
        
        # Serialize any non-json types (simple version)
        doc_to_save = json.loads(json.dumps(document, default=str))
        data.append(doc_to_save)
        self._save_data(data)
        
        class InsertResult:
            def __init__(self, id):
                self.inserted_id = id
        return InsertResult(doc_to_save["_id"])

    async def update_one(self, filter: Dict, update: Dict, upsert: bool = False):
        data = self._get_data()
        found = False
        for i, item in enumerate(data):
            match = True
            for k, v in filter.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                if "$set" in update:
                    item.update(update["$set"])
                else:
                    item.update(update)
                data[i] = item
                found = True
                break
        
        if not found and upsert:
            new_doc = filter.copy()
            if "$set" in update:
                new_doc.update(update["$set"])
            else:
                new_doc.update(update)
            data.append(new_doc)
            
        self._save_data(data)

class JsonDatabase:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = {}
        else:
            self.data = {}

    def _save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4, default=str)

    def __getattr__(self, name: str) -> JsonCollection:
        return JsonCollection(self, name)

class JsonClient:
    def __init__(self, file_path: str = "db.json"):
        self.db = JsonDatabase(file_path)

    def __getattr__(self, name: str) -> JsonDatabase:
        return self.db

    def close(self):
        pass
