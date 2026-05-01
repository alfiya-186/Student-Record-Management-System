import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()

from core.models import Course, Subject

def seed_expert_programs():
    print("Seeding institutional programs...")
    
    # 3-Year Program
    bba, created = Course.objects.get_or_create(
        code="BBA-MGT", 
        defaults={'name': "Bachelor of Business Administration", 'duration': 3}
    )
    if created:
        Subject.objects.create(course=bba, name="Financial Accounting")
        Subject.objects.create(course=bba, name="Business Ethics")
        Subject.objects.create(course=bba, name="Organizational Behavior")
        print(f"Added {bba.name}")

    # 5-Year Program
    law, created = Course.objects.get_or_create(
        code="BA-LLB", 
        defaults={'name': "Integrated Law Degree (B.A. LL.B)", 'duration': 5}
    )
    if created:
        Subject.objects.create(course=law, name="Jurisprudence")
        Subject.objects.create(course=law, name="Constitutional Law")
        Subject.objects.create(course=law, name="Criminal Procedure")
        Subject.objects.create(course=law, name="International Trade Law")
        print(f"Added {law.name}")

if __name__ == "__main__":
    seed_expert_programs()
