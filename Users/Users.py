from pymongo import MongoClient
from faker import Faker
from datetime import datetime
import random

fake = Faker()

client = MongoClient('mongodb://localhost:27017/')
db = client["social_media"]
users_collection = db["users"]

def generate_object_id():
    return ''.join(random.choices('0123456789abcdef', k=24))

users = []
user_ids = [] 
for _ in range(400):
    user_id = generate_object_id()
    user_ids.append(user_id)  
    joined_groups = [
        {
            "name": fake.word() + " " + fake.word(),
            "description": fake.sentence()
        }
    ]
    messages = [
        {
            "sender_id": user_id,
            "receiver_id": generate_object_id(),
            "message": fake.sentence(),
            "created_at": fake.date_time_this_year().isoformat() + "Z"
        },
        {
            "sender_id": generate_object_id(),
            "receiver_id": user_id,
            "message": fake.sentence(),
            "created_at": fake.date_time_this_year().isoformat() + "Z"
        }
    ]
    notifications = [
        {
            "type": random.choice(["like", "comment", "follow"]),
            "details": {
                "post_id": generate_object_id(),
                "liked_by": generate_object_id()
            },
            "read": False,
            "created_at": fake.date_time_this_year().isoformat() + "Z"
        }
    ]
    
    followers = [
        {
            "follower_id": random.choice(user_ids),
            "followed_at": fake.date_time_this_year().isoformat() + "Z"
        }
        for _ in range(random.randint(0, 10))
    ]
    
    user = {
        "user_id": user_id,
        "name": fake.first_name(),
        "joined_groups": joined_groups,
        "messages": messages,
        "notifications": notifications,
        "followers": followers
    }
    users.append(user)

users_collection.insert_many(users)
print("400 user documents inserted into the 'users' collection.")
