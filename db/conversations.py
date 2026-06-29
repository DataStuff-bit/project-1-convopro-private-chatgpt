import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from pymongo import DESCENDING
from db.mongo import get_collection

conversations = get_collection("conversation")
conversations.create_index([("last_interacted", DESCENDING)])

# --HELPERS---
def now_utc():
    return datetime.now(timezone.utc)

def create_new_conversation_id() -> str:
    return str(uuid.uuid4())

# Delete --------------------
def delete_conversation(conv_id: str):
    conversations.delete_one({"_id": conv_id})  # FIX 1: use conversations, no ObjectId (uuid string)

# Core services -------------
def create_new_conversation(title: Optional[str] = None, role: Optional[str] = None, content: Optional[str] = None) -> str:
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],  # FIX 2: was "message", should be "messages"
        "last_interacted": ts,
    }
    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})  # FIX 3: "message" → "messages"
    conversations.insert_one(doc)
    return conv_id

def add_message(conv_id: str, role: str, content: str) -> bool:
    ts = now_utc()
    res = conversations.update_one(
        {"_id": conv_id},  # FIX 4: was "id", should be "_id"
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts},
        },
    )
    return res.matched_count == 1

def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id": conv_id},  # FIX 5: was "id", should be "_id"
        {"$set": {"last_interacted": ts}},
        return_document=True,
    )
    return doc

def get_all_conversations() -> Dict[str, str]:
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return {doc["_id"]: doc["title"] for doc in cursor}