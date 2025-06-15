from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import string

# MongoDB connection
uri = "mongodb+srv://adesuwaola16:u81Fgz7AsFmr8Gb9@cluster0.wunrjfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['eduhub_db']

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def create_sample_users():
    users = []
    roles = ['student', 'instructor']
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'James', 'Lisa', 'Robert', 'Mary',
                   'Chris', 'Anna', 'Brian', 'Olivia', 'Kevin', 'Sophia', 'Daniel', 'Mia', 'Matthew', 'Ella']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    # Create 20 users (15 students, 5 instructors)
    for i in range(20):
        role = 'instructor' if i < 5 else 'student'
        user = {
            'userId': generate_id(),
            'email': f"{first_names[i].lower()}.{last_names[i].lower()}@example.com",
            'firstName': first_names[i],
            'lastName': last_names[i],
            'role': role,
            'dateJoined': datetime.now() - timedelta(days=random.randint(1, 365)),
            'profile': {
                'bio': f"Professional {role} with expertise in various fields",
                'avatar': f"https://example.com/avatars/{i}.jpg",
                'skills': ['Python', 'JavaScript', 'Data Science', 'Web Development']
            },
            'isActive': True
        }
        users.append(user)
    
    db.users.insert_many(users)
    return users

def create_sample_courses(users):
    courses = []
    categories = ['Programming', 'Data Science', 'Web Development', 'Mobile Development', 'Design']
    levels = ['beginner', 'intermediate', 'advanced']
    
    # Get instructor IDs
    instructor_ids = [user['userId'] for user in users if user['role'] == 'instructor']
    
    # Create 8 courses
    for i in range(8):
        course = {
            'courseId': generate_id(),
            'title': f"Course {i+1}: {random.choice(categories)} Masterclass",
            'description': f"Comprehensive course on {random.choice(categories)}",
            'instructorId': random.choice(instructor_ids),
            'category': random.choice(categories),
            'level': random.choice(levels),
            'duration': float(random.randint(10, 40)),
            'price': float(random.randint(50, 200)),
            'tags': random.sample(['Python', 'JavaScript', 'Data Science', 'Web Development', 'Mobile', 'Design'], 3),
            'createdAt': datetime.now() - timedelta(days=random.randint(1, 180)),
            'updatedAt': datetime.now(),
            'isPublished': True
        }
        courses.append(course)
    
    db.courses.insert_many(courses)
    return courses

def create_sample_enrollments(users, courses):
    enrollments = []
    student_ids = [user['userId'] for user in users if user['role'] == 'student']
    
    # Create 15 enrollments, ensuring no duplicate (userId, courseId) pairs
    used_pairs = set()
    attempts = 0
    while len(enrollments) < 15 and attempts < 100:
        user_id = random.choice(student_ids)
        course_id = random.choice(courses)['courseId']
        pair = (user_id, course_id)
        if pair not in used_pairs:
            enrollment = {
                'userId': user_id,
                'courseId': course_id,
                'enrollmentDate': datetime.now() - timedelta(days=random.randint(1, 90)),
                'completionStatus': random.choice(['not_started', 'in_progress', 'completed']),
                'progress': random.randint(0, 100)
            }
            enrollments.append(enrollment)
            used_pairs.add(pair)
        attempts += 1
    
    db.enrollments.insert_many(enrollments)

def create_sample_lessons(courses):
    lessons = []
    
    # Create 25 lessons across all courses
    for course in courses:
        num_lessons = random.randint(3, 5)
        for i in range(num_lessons):
            lesson = {
                'courseId': course['courseId'],
                'title': f"Lesson {i+1}: {random.choice(['Introduction', 'Advanced Topics', 'Practical Examples', 'Case Studies'])}",
                'content': f"Detailed content for lesson {i+1}",
                'order': i + 1,
                'duration': random.randint(30, 120)
            }
            lessons.append(lesson)
    
    db.lessons.insert_many(lessons)

def create_sample_assignments(courses):
    assignments = []
    
    # Create 10 assignments across all courses
    for course in courses:
        num_assignments = random.randint(1, 2)
        for i in range(num_assignments):
            assignment = {
                'assignmentId': generate_id(),
                'courseId': course['courseId'],
                'title': f"Assignment {i+1}: {random.choice(['Project', 'Quiz', 'Homework'])}",
                'description': f"Detailed instructions for assignment {i+1}",
                'dueDate': datetime.now() + timedelta(days=random.randint(7, 30)),
                'maxScore': 100
            }
            assignments.append(assignment)
    
    db.assignments.insert_many(assignments)
    # Retrieve assignments from DB to ensure assignmentId is present
    return list(db.assignments.find())

def create_sample_submissions(users, assignments):
    submissions = []
    student_ids = [user['userId'] for user in users if user['role'] == 'student']
    
    # Create 12 submissions
    for _ in range(12):
        assignment = random.choice(assignments)
        submission = {
            'assignmentId': assignment['assignmentId'],
            'userId': random.choice(student_ids),
            'submissionDate': datetime.now() - timedelta(days=random.randint(1, 14)),
            'content': f"Submission content for assignment {assignment['title']}",
            'score': random.randint(60, 100),
            'feedback': "Good work! Keep it up."
        }
        submissions.append(submission)
    
    db.submissions.insert_many(submissions)

def main():
    print("Populating database with sample data...")
    
    # Clear collections before inserting new data
    db.users.delete_many({})
    db.courses.delete_many({})
    db.enrollments.delete_many({})
    db.lessons.delete_many({})
    db.assignments.delete_many({})
    db.submissions.delete_many({})
    
    # Create and insert sample data
    users = create_sample_users()
    print("Created sample users")
    
    courses = create_sample_courses(users)
    print("Created sample courses")
    
    create_sample_enrollments(users, courses)
    print("Created sample enrollments")
    
    create_sample_lessons(courses)
    print("Created sample lessons")
    
    assignments = create_sample_assignments(courses)
    print("Created sample assignments")
    
    create_sample_submissions(users, assignments)
    print("Created sample submissions")
    
    print("Database population completed successfully!")

if __name__ == "__main__":
    main() 