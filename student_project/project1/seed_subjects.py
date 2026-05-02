import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()

from core.models import Course, Subject

def seed_subjects():
    print("Seeding subjects for existing courses...")
    courses = Course.objects.all()
    
    # Generic subjects to add to any course that doesn't have them
    default_subjects = [
        "Core Theory",
        "Practical Application",
        "Research Methodology",
        "Final Project"
    ]
    
    for course in courses:
        # Check if course already has subjects
        if course.subjects.count() == 0:
            print(f"Adding subjects to {course.name}...")
            for sub_name in default_subjects:
                Subject.objects.create(course=course, name=sub_name)
            print(f"Added 4 subjects to {course.name}")
        else:
            print(f"{course.name} already has {course.subjects.count()} subjects. Skipping.")
            
    print("Subject seeding complete!")

if __name__ == '__main__':
    seed_subjects()
