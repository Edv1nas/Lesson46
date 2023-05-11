from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from typing import Dict, Any, List


class LibraryManager:
    def __init__(self, host: str, port: int, db_name: str, collection_name: str):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_book(self, book: Dict[str, Any]) -> str:
        result = self.collection.insert_one(book)
        return str(result.inserted_id)

    def get_all_books(self) -> List[Dict[str, Any]]:
        return list(self.collection.find())

    def get_book(self, book_id: str) -> Dict[str, Any]:
        objInstance = ObjectId(book_id)
        return self.collection.find_one({"_id": objInstance})

    def update_book(self, book_id: str, updates: Dict[str, Any]) -> bool:
        objInstance = ObjectId(book_id)
        result = self.collection.update_one(
            {"_id": objInstance}, {"$set": updates})
        return result.modified_count > 0

    def delete_book(self, book_id: str) -> bool:
        objInstance = ObjectId(book_id)
        result = self.collection.delete_one({"_id": objInstance})
        return result.deleted_count > 0


library = LibraryManager(host="localhost", port=27017,
                         db_name="Libary", collection_name="Fantasy books")

book = {
    "title": "Harry Potter and the Chamber of Secrets",
    "author": "J.K. Rowling",
    "year": 1998
}

# inserted_id = library.add_book(book)
# print("Inserted ID:", inserted_id)

# all_books = library.get_all_books()
# print("All Books:", all_books)

book_id = "645d2b4b245edc8b710edaca"
specific_book = library.get_book(book_id)
print("Specific Book:", specific_book)

# updates = {"year": 2022}
# is_updated = library.update_book(book_id, updates)
# print("Is Updated:", is_updated)

is_deleted = library.delete_book(book_id)
print("Is Deleted:", is_deleted)
