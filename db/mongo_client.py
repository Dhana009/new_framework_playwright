import os
from pymongo import MongoClient


class MongoSeedCleaner:
    """
    MongoDB utility for cleaning seed data.

    Responsibilities:
    - Connect to MongoDB using MONGODB_URI
    - Hard-delete seed data ONLY
    - No business logic
    - No test orchestration logic
    """

    def __init__(self):
        mongo_uri = os.environ.get("MONGODB_URI")
        if not mongo_uri:
            raise RuntimeError("MONGODB_URI is not set")

        self.client = MongoClient(mongo_uri)

        # Database name is derived from the URI (flowhub / flowhub-test)
        self.db = self.client.get_default_database()

        # Confirmed collection name
        self.items = self.db["items"]

    def delete_all_seed_items(self):
        """
        Delete all seed-tagged items (global reset).
        """
        self.items.delete_many({
            "tags": {"$in": ["seed"]}
        })

    def delete_editor_seed_items(self, editor_id):
        """
        Delete seed-tagged items created by a specific editor.
        """
        self.items.delete_many({
            "tags": {"$in": ["seed"]},
            "created_by": editor_id
        })
