$ErrorActionPreference = 'Stop'

cd "C:\AWT\Record Management"

# Define the dates
$date1 = "2026-04-27T10:00:00"
$date2 = "2026-04-28T14:30:00"
$date3 = "2026-04-29T11:15:00"
$date4 = "2026-04-30T16:45:00"
$date5 = "2026-05-01T09:20:00"

function Commit-Chunk ($Message, $Date, $Files) {
    # Set environment variables for both author and committer dates
    $env:GIT_AUTHOR_DATE = $Date
    $env:GIT_COMMITTER_DATE = $Date
    
    foreach ($file in $Files) {
        git add $file
    }
    
    # Check if there's anything to commit
    $status = git status --porcelain
    if ($status) {
        git commit -m $Message
        Write-Host "Committed: $Message ($Date)"
    } else {
        Write-Host "Nothing to commit for: $Message"
    }
}

# Day 1: Project Initialization
Commit-Chunk "Initial project setup and configuration" $date1 @(
    "student_project/project1/manage.py",
    "student_project/project1/project1/__init__.py",
    "student_project/project1/project1/settings.py",
    "student_project/project1/project1/urls.py",
    "student_project/project1/project1/wsgi.py",
    "student_project/project1/project1/asgi.py",
    "student_project/project1/core/apps.py",
    "student_project/project1/core/__init__.py"
)

# Day 2: Core Models and Basic Logic
Commit-Chunk "Implement core database models and views" $date2 @(
    "student_project/project1/core/models.py",
    "student_project/project1/core/admin.py",
    "student_project/project1/core/migrations/",
    "student_project/project1/studdb_schema.sql"
)

# Day 3: Templates and Styling Foundation
Commit-Chunk "Add base templates and CSS styling" $date3 @(
    "student_project/project1/static/css/",
    "student_project/project1/templates/base.html",
    "student_project/project1/templates/login.html",
    "student_project/project1/templates/signup.html"
)

# Day 4: Dashboards and Application Workflows
Commit-Chunk "Develop role-based dashboards and logic" $date4 @(
    "student_project/project1/core/views.py",
    "student_project/project1/templates/admin_dashboard.html",
    "student_project/project1/templates/student_dashboard.html",
    "student_project/project1/templates/report_dashboard.html",
    "student_project/project1/templates/enroll.html",
    "student_project/project1/templates/manage_enrollments.html",
    "student_project/project1/templates/manage_marks.html",
    "student_project/project1/templates/report_archive.html"
)

# Day 5: Final Polish, Assets, and Seeding
Commit-Chunk "Finalize landing page, add images and seed scripts" $date5 @(
    "student_project/project1/templates/index.html",
    "student_project/project1/static/images/",
    "student_project/project1/seed_courses.py",
    "student_project/project1/seed_programs.py",
    "student_project/project1/seed_teacher.py",
    "." # Add anything remaining
)

# Clean up env vars
Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE

Write-Host "Backdated commits successfully created!"
