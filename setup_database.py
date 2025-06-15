from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
uri = "mongodb+srv://adesuwaola16:u81Fgz7AsFmr8Gb9@cluster0.wunrjfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['eduhub_db']

# Schema definitions
user_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["email", "firstName", "lastName", "role", "dateJoined"],
            "properties": {
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                },
                "firstName": {"bsonType": "string"},
                "lastName": {"bsonType": "string"},
                "role": {
                    "enum": ["student", "instructor"]
                },
                "dateJoined": {"bsonType": "date"},
                "profile": {
                    "bsonType": "object",
                    "properties": {
                        "bio": {"bsonType": "string"},
                        "avatar": {"bsonType": "string"},
                        "skills": {
                            "bsonType": "array",
                            "items": {"bsonType": "string"}
                        }
                    }
                },
                "isActive": {"bsonType": "bool"}
            }
        }
    }
}

course_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "instructorId", "category", "level", "price"],
            "properties": {
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "instructorId": {"bsonType": "string"},
                "category": {"bsonType": "string"},
                "level": {
                    "enum": ["beginner", "intermediate", "advanced"]
                },
                "duration": {"bsonType": "number"},
                "price": {"bsonType": "number"},
                "tags": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                },
                "createdAt": {"bsonType": "date"},
                "updatedAt": {"bsonType": "date"},
                "isPublished": {"bsonType": "bool"}
            }
        }
    }
}

enrollment_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["userId", "courseId", "enrollmentDate"],
            "properties": {
                "userId": {"bsonType": "string"},
                "courseId": {"bsonType": "string"},
                "enrollmentDate": {"bsonType": "date"},
                "completionStatus": {"bsonType": "string"},
                "progress": {"bsonType": "number"}
            }
        }
    }
}

lesson_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["courseId", "title", "content", "order"],
            "properties": {
                "courseId": {"bsonType": "string"},
                "title": {"bsonType": "string"},
                "content": {"bsonType": "string"},
                "order": {"bsonType": "int"},
                "duration": {"bsonType": "number"}
            }
        }
    }
}

assignment_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["courseId", "title", "dueDate"],
            "properties": {
                "courseId": {"bsonType": "string"},
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "dueDate": {"bsonType": "date"},
                "maxScore": {"bsonType": "number"}
            }
        }
    }
}

submission_schema = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["assignmentId", "userId", "submissionDate"],
            "properties": {
                "assignmentId": {"bsonType": "string"},
                "userId": {"bsonType": "string"},
                "submissionDate": {"bsonType": "date"},
                "content": {"bsonType": "string"},
                "score": {"bsonType": "number"},
                "feedback": {"bsonType": "string"}
            }
        }
    }
}

def create_collections():
    # Create collections with schema validation
    collections = {
        'users': user_schema,
        'courses': course_schema,
        'enrollments': enrollment_schema,
        'lessons': lesson_schema,
        'assignments': assignment_schema,
        'submissions': submission_schema
    }
    
    for collection_name, schema in collections.items():
        try:
            db.create_collection(collection_name, validator=schema['validator'])
            print(f"Created collection: {collection_name}")
        except Exception as e:
            print(f"Collection {collection_name} might already exist: {str(e)}")

def create_indexes():
    # Users collection indexes
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.users.create_index([("role", ASCENDING)])
    
    # Courses collection indexes
    db.courses.create_index([("title", "text"), ("description", "text")])
    db.courses.create_index([("category", ASCENDING)])
    db.courses.create_index([("instructorId", ASCENDING)])
    
    # Enrollments collection indexes
    db.enrollments.create_index([("userId", ASCENDING), ("courseId", ASCENDING)], unique=True)
    
    # Lessons collection indexes
    db.lessons.create_index([("courseId", ASCENDING), ("order", ASCENDING)])
    
    # Assignments collection indexes
    db.assignments.create_index([("courseId", ASCENDING), ("dueDate", ASCENDING)])
    
    # Submissions collection indexes
    db.submissions.create_index([("assignmentId", ASCENDING), ("userId", ASCENDING)])

def main():
    print("Setting up EduHub database...")
    create_collections()
    create_indexes()
    print("Database setup completed successfully!")

if __name__ == "__main__":
    main() 