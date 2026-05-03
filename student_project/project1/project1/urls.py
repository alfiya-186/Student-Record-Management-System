from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('signup/', views.signup),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    
    # Student
    path('student_dashboard/', views.student_dashboard),
    path('enroll/', views.enroll_course),
    
    # Admin - Courses
    path('manage_courses/', views.manage_courses),
    path('add_course/', views.add_course),
    path('delete_course/<int:course_id>/', views.delete_course),
    
    # Admin - Students
    path('admin_dashboard/', views.admin_dashboard),
    path('manage_enrollments/', views.manage_enrollments),
    path('process_enrollment/<int:enrollment_id>/<str:action>/', views.process_enrollment),
    path('manage_marks/', views.manage_marks),
    path('enter_marks/<int:enrollment_id>/', views.enter_marks),
    
    # Reports
    path('report_dashboard/', views.report_dashboard),
    path('report_archive/', views.report_archive),
    path('course_report/<int:course_id>/', views.course_detail_report),
    path('generate_report/<int:enrollment_id>/', views.generate_report),
]