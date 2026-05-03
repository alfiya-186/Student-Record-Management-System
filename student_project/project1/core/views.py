from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, UserProfile, Course, Enrollment, Subject, SubjectMark, PerformanceReport
from django.db.models import Avg, Count, Q

def index(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user, role='student')
            messages.info(request, "Your account profile has been automatically initialized as a Student.")
        
        if profile.role == 'admin': return redirect('/admin_dashboard/')
        elif profile.role == 'student': return redirect('/student_dashboard/')
        elif profile.role == 'report': return redirect('/report_dashboard/')
            
    return render(request, 'index.html')

def signup(request):
    if request.user.is_authenticated: return redirect('/')
    courses = Course.objects.all()
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        gender = request.POST.get('gender', 'other')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role', 'student')
        
        username = email # Use email as the unique username

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "An account with this email already exists")
        else:
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserProfile.objects.create(user=user, role=role)
            if role == 'student':
                reg_no = f"REG-{User.objects.count():05d}"
                Student.objects.create(user=user, full_name=full_name, gender=gender, reg_no=reg_no)
            
            messages.success(request, "Registration successful. Please login.")
            return redirect('/login/')
    return render(request, 'signup.html', {'courses': courses})

def user_login(request):
    if request.user.is_authenticated: return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

# --- STUDENT ROLE ---

@login_required
def student_dashboard(request):
    if request.user.userprofile.role != 'student': return redirect('/')
    
    enrollments = Enrollment.objects.filter(student=request.user).order_by('-date_enrolled')
    return render(request, 'student_dashboard.html', {'enrollments': enrollments})

@login_required
def enroll_course(request):
    if request.user.userprofile.role != 'student': return redirect('/')
    
    if request.method == 'POST':
        course_id = request.POST['course']
        year = int(request.POST['year'])
        course = get_object_or_404(Course, id=course_id)
        
        # Validation: Check duration
        if year > course.duration:
            messages.error(request, f"This program only lasts {course.duration} years. You cannot enroll in Year {year}.")
        elif Enrollment.objects.filter(student=request.user, course=course, status='pending').exists():
            messages.warning(request, "You already have a pending application for this course.")
        else:
            Enrollment.objects.create(student=request.user, course=course, year_of_study=year)
            messages.success(request, f"Enrollment requested for {course.name}! Wait for admin approval.")
            return redirect('/student_dashboard/')
            
    courses = Course.objects.all()
    return render(request, 'enroll.html', {'courses': courses})

# --- ADMIN ROLE ---

@login_required
def admin_dashboard(request):
    if request.user.userprofile.role != 'admin': return redirect('/')
    
    pending_count = Enrollment.objects.filter(status='pending').count()
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    return render(request, 'admin_dashboard.html', {
        'pending_count': pending_count, 
        'total_students': total_students,
        'total_courses': total_courses
    })

@login_required
def manage_courses(request):
    if request.user.userprofile.role != 'admin': return redirect('/')
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.user.userprofile.role != 'admin': return redirect('/')
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        duration = request.POST['duration']
        subjects_raw = request.POST.get('subjects', '')
        
        course = Course.objects.create(name=name, code=code, duration=duration)
        
        # Add subjects
        if subjects_raw:
            subject_names = [s.strip() for s in subjects_raw.split(',') if s.strip()]
            for s_name in subject_names:
                Subject.objects.create(course=course, name=s_name)
        
        messages.success(request, f"Program '{name}' successfully created.")
        return redirect('/manage_courses/')
    return render(request, 'add_course.html')

@login_required
def delete_course(request, course_id):
    if request.user.userprofile.role != 'admin': return redirect('/')
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Program removed from catalog.")
    return redirect('/manage_courses/')

@login_required
def manage_enrollments(request):
    if request.user.userprofile.role != 'admin': return redirect('/')
    
    enrollments = Enrollment.objects.filter(status='pending').order_by('-date_enrolled')
    return render(request, 'manage_enrollments.html', {'enrollments': enrollments})

@login_required
def process_enrollment(request, enrollment_id, action):
    if request.user.userprofile.role != 'admin': return redirect('/')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if action == 'accept':
        enrollment.status = 'accepted'
        messages.success(request, f"Accepted {enrollment.student.username}'s enrollment.")
    else:
        enrollment.status = 'rejected'
        messages.info(request, f"Rejected {enrollment.student.username}'s enrollment.")
    enrollment.save()
    return redirect('/manage_enrollments/')

@login_required
def manage_marks(request):
    if request.user.userprofile.role != 'admin': return redirect('/')
    
    # List all accepted enrollments
    enrollments = Enrollment.objects.filter(status='accepted').order_by('course', 'student__username')
    return render(request, 'manage_marks.html', {'enrollments': enrollments})

@login_required
def enter_marks(request, enrollment_id):
    if request.user.userprofile.role != 'admin': return redirect('/')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    subjects = enrollment.course.subjects.all()
    
    if request.method == 'POST':
        for subject in subjects:
            mark_val = request.POST.get(f'subject_{subject.id}', 0)
            try:
                mark_val = int(mark_val)
            except (ValueError, TypeError):
                mark_val = 0
                
            SubjectMark.objects.update_or_create(
                enrollment=enrollment, subject=subject,
                defaults={'marks': mark_val}
            )
        messages.success(request, f"Marks updated and rating calculated for {enrollment.student.username}.")
        return redirect('/manage_marks/')
        
    current_marks = {sm.subject_id: sm.marks for sm in SubjectMark.objects.filter(enrollment=enrollment)}
    return render(request, 'enter_marks.html', {'enrollment': enrollment, 'subjects': subjects, 'current_marks': current_marks})

# --- REPORT ROLE ---

@login_required
def report_dashboard(request):
    if not (request.user.userprofile.role in ['report', 'admin']): return redirect('/')
    
    course_stats = Course.objects.annotate(student_count=Count('enrollment')).order_by('-student_count')
    
    # Pass/Fail calculation (Threshold 40%)
    all_gradable_enrollments = Enrollment.objects.filter(status='accepted')
    passed_count = 0
    failed_count = 0
    
    for e in all_gradable_enrollments:
        passed = e.is_passed
        if passed is True: passed_count += 1
        elif passed is False: failed_count += 1
            
    return render(request, 'report_dashboard.html', {
        'course_stats': course_stats,
        'passed_count': passed_count,
        'failed_count': failed_count
    })

@login_required
def report_archive(request):
    if not (request.user.userprofile.role in ['report', 'admin']): return redirect('/')
    
    query = request.GET.get('q', '').strip()
    
    # Validation: limit query length to prevent excessive resource usage
    if len(query) > 100:
        query = query[:100]
        
    enrollments = Enrollment.objects.all().order_by('-date_enrolled')
    
    if query:
        enrollments = enrollments.filter(
            Q(student__username__icontains=query) |
            Q(student__student__full_name__icontains=query) |
            Q(student__student__reg_no__icontains=query) |
            Q(course__name__icontains=query)
        ).distinct()
        
    return render(request, 'report_archive.html', {'enrollments': enrollments, 'query': query})

@login_required
def course_detail_report(request, course_id):
    if not (request.user.userprofile.role in ['report', 'admin']): return redirect('/')
    
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).order_by('status', 'student__username')
    return render(request, 'course_report.html', {'course': course, 'enrollments': enrollments})

# --- GENERATE REPORT ---

@login_required
def generate_report(request, enrollment_id):
    if not (request.user.userprofile.role in ['report', 'admin']): return redirect('/')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if enrollment.status != 'accepted':
        messages.error(request, "Reports can only be generated for accepted enrollments.")
        return redirect('/report_archive/')
    
    marks = enrollment.subject_marks.all()
    if not marks.exists():
        messages.error(request, f"No marks have been entered yet for {enrollment.student.username}. Please enter marks first.")
        return redirect('/report_archive/')
    
    percentage = round(enrollment.average_percentage, 2)
    rating     = enrollment.performance_rating
    grade      = PerformanceReport.compute_grade(percentage)
    passed     = percentage >= 40
    remarks    = PerformanceReport.compute_remarks(percentage)
    
    report, created = PerformanceReport.objects.update_or_create(
        enrollment=enrollment,
        defaults={
            'generated_by': request.user,
            'percentage':   percentage,
            'rating':       rating,
            'grade':        grade,
            'is_passed':    passed,
            'remarks':      remarks,
        }
    )
    
    action = "Generated" if created else "Updated"
    messages.success(request, f"Report {action}: {enrollment.student.username} — {enrollment.course.name} [{grade}]")
    return redirect('/report_archive/')
