import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()

from core.models import Course

def seed_courses():
    courses_data = [
        {"name": "Computer Science & Engineering", "code": "CSE-101", "duration": 4},
        {"name": "Business Administration", "code": "BBA-201", "duration": 3},
        {"name": "Data Science & AI", "code": "DSAI-301", "duration": 4},
        {"name": "Mechanical Engineering", "code": "ME-401", "duration": 4},
        {"name": "Bachelor of Arts in Economics", "code": "BA-ECO-501", "duration": 3},
        {"name": "Information Technology", "code": "IT-601", "duration": 4},
    ]

    for data in courses_data:
        course, created = Course.objects.get_or_create(code=data["code"], defaults={
            "name": data["name"],
            "duration": data["duration"]
        })
        if created:
            print(f"Created course: {course.name} ({course.duration} years)")
        else:
            print(f"Course already exists: {course.name}")

if __name__ == '__main__':
    print("Seeding courses...")
    seed_courses()
    print("Done.")
