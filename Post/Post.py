from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

client = MongoClient('mongodb://localhost:27017/')
db = client['social_media']
posts_collection = db['posts']
users_collection = db['users']

def generate_object_id():
    return ''.join(random.choices('0123456789abcdef', k=24))

user_ids = [user["user_id"] for user in users_collection.find({}, {"_id": 0, "user_id": 1})]

records = []
base_created_at = datetime.strptime("2024-06-10T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

for i in range(400):
    post_id = generate_object_id()
    author_id = random.choice(user_ids)  
    content = fake.sentence()  
    created_at = base_created_at + timedelta(seconds=i)
    
    comments = []
    num_comments = random.randint(1, 5)  
    for _ in range(num_comments):
        comment_id = generate_object_id()
        commenter_id = random.choice(user_ids)
        comment_content = fake.sentence()
        comment_created_at = created_at + timedelta(seconds=random.randint(1, 60)) 
        comment = {
            "comment_id": comment_id,
            "author_id": commenter_id,
            "content": comment_content,
            "created_at": comment_created_at.isoformat() + 'Z'
        }
        comments.append(comment)

    likes = [generate_object_id(), generate_object_id()]

    record = {
        "post_id": post_id,
        "author_id": author_id,
        "content": content,
        "created_at": created_at.isoformat() + 'Z',
        "comments": comments,
        "likes": likes
    }

    records.append(record)

posts_collection.insert_many(records)

print("400 Records inserted to `posts` successfully.")
