from pymongo import MongoClient
import json
from bson import json_util
from datetime import datetime

# MongoDB connection
uri = "mongodb+srv://adesuwaola16:u81Fgz7AsFmr8Gb9@cluster0.wunrjfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['eduhub_db']

def export_collection(collection_name):
    """Export a collection to a list of documents"""
    collection = db[collection_name]
    return list(collection.find())

def main():
    # Export all collections
    collections = {
        'users': export_collection('users'),
        'courses': export_collection('courses'),
        'enrollments': export_collection('enrollments'),
        'lessons': export_collection('lessons'),
        'assignments': export_collection('assignments'),
        'submissions': export_collection('submissions')
    }
    
    # Write to JSON file
    with open('sample_data.json', 'w') as f:
        json.dump(collections, f, default=json_util.default, indent=2)
    
    print("Data exported successfully to sample_data.json")

if __name__ == "__main__":
    main() 