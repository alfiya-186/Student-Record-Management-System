from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('report', 'Report Viewer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration = models.IntegerField(default=4) # Total years of study

    def __str__(self):
        return f"{self.name} ({self.duration} years)"

class Subject(models.Model):
    course = models.ForeignKey(Course, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class Student(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    reg_no = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.full_name or self.user.username} - {self.reg_no}"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year_of_study = models.IntegerField() # Validated against course.duration
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name} ({self.status})"

    @property
    def performance_rating(self):
        marks = self.subject_marks.all()
        if not marks.exists():
            return 0.0
        avg_score = marks.aggregate(Avg('marks'))['marks__avg']
        return round((avg_score / 100) * 5, 1) if avg_score else 0.0

    @property
    def average_percentage(self):
        marks = self.subject_marks.all()
        if not marks.exists():
            return 0.0
        return marks.aggregate(Avg('marks'))['marks__avg'] or 0.0

    @property
    def is_passed(self):
        # Pass if marks are entered and average is >= 40%
        marks = self.subject_marks.all()
        if not marks.exists():
            return None # Not yet graded
        return self.average_percentage >= 40

class SubjectMark(models.Model):
    enrollment = models.ForeignKey(Enrollment, related_name='subject_marks', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('enrollment', 'subject')

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.subject.name}: {self.marks}"