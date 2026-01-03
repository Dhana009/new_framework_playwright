import random
import uuid
from datetime import datetime


def build_flow3_items(created_by: str | None = None) -> list[dict]:
    """
    Build seed payloads for Flow 3.

    Characteristics:
    - Supports pagination, search, filter, sort
    - Covers all item_type variants
    - Can be reused for admin or editor seed
    - Does NOT perform API calls

    Args:
        created_by: user id (optional)
                    - None → admin/global seed
                    - str  → editor-owned seed

    Returns:
        List of item payload dicts
    """

    items = []

    item_types = ["PHYSICAL", "DIGITAL", "SERVICE"]
    categories = ["Electronics", "Books", "Services", "Office"]

    for index in range(31):  # Flow 3 requires 31+ items
        item_type = random.choice(item_types)

        base_item = {
            "name": f"Item {index} {uuid.uuid4().hex[:6]}",
            "description": f"Description for item {index}",
            "item_type": item_type,
            "price": round(random.uniform(10, 500), 2),
            "category": random.choice(categories),
            "normalizedCategory": "general",
            "is_active": index % 2 == 0,
            "version": 1,
            "created_by": created_by,
            "tags": ["seed", "flow3"],
            "createdAt": datetime.utcnow().isoformat(),
        }

        # Conditional fields
        if item_type == "PHYSICAL":
            base_item.update({
                "weight": round(random.uniform(0.5, 10), 2),
                "dimensions": {
                    "length": round(random.uniform(10, 100), 1),
                    "width": round(random.uniform(10, 100), 1),
                    "height": round(random.uniform(1, 50), 1),
                },
            })

        elif item_type == "DIGITAL":
            base_item.update({
                "download_url": "https://example.com/download/file.zip",
                "file_size": random.randint(1000, 5_000_000),
            })

        elif item_type == "SERVICE":
            base_item.update({
                "duration_hours": random.randint(1, 40),
            })

        # Optional fields (realistic but non-essential)
        if index % 3 == 0:
            base_item["embed_url"] = "https://example.com/embed/demo"

        if index % 4 == 0:
            base_item["file_path"] = f"uploads/items/{uuid.uuid4().hex}.pdf"
            base_item["file_metadata"] = {
                "original_name": "document.pdf",
                "content_type": "application/pdf",
                "size": random.randint(1000, 500_000),
                "uploaded_at": datetime.utcnow().isoformat(),
            }

        items.append(base_item)

    return items
