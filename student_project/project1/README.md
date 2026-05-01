# EduCore | Student Record Management System

A high-fidelity, centralized governance platform for modern educational institutions. This system provides comprehensive oversight of the academic lifecycle, from student registration to performance analytics and reporting.

## 🚀 Key Features

*   **Immersive Landing Page**: Professional institution portal with dynamic background cross-fades and institutional gallery.
*   **Role-Based Dashboards**: Tailored interfaces for Administrators, Students, and Academic Auditors.
*   **Smart Registration**: Dynamic signup flow with real-time course duration detection and institutional validation.
*   **Admission Management**: Centralized queue for reviewing and processing student enrollment applications.
*   **Performance Analytics**: Automated grade benchmarks, subject-level mark entry, and comprehensive academic reporting.
*   **Robust Backend**: Powered by Django and MySQL for secure, scalable data management.

## 🛠️ Technology Stack

*   **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism design), JavaScript (ES6+).
*   **Backend**: Python, Django.
*   **Database**: MySQL (Production-ready).
*   **Media**: AI-generated architectural institutional photography.

## 📦 Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/alfiya-186/Student-Record-Management-System.git
    ```
2.  **Install dependencies**:
    ```bash
    pip install django mysqlclient
    ```
3.  **Database Configuration**:
    *   Create a MySQL database named `studdb`.
    *   Update `project1/settings.py` with your MySQL credentials.
4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Seed Data**:
    ```bash
    python seed_courses.py
    ```
6.  **Launch Server**:
    ```bash
    python manage.py runserver
    ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
*Developed with focus on academic excellence and institutional efficiency.*
