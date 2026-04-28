-- MySQL Database Schema for 'studdb'
-- This file shows the 'code' for your database tables.

CREATE DATABASE IF NOT EXISTS studdb;
USE studdb;

-- Table for User Roles
CREATE TABLE core_userprofile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(20) NOT NULL,
    user_id INT UNIQUE NOT NULL
);

-- Table for Academic Courses
CREATE TABLE core_course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    duration INT DEFAULT 4
);

-- Table for Student Details
CREATE TABLE core_student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_no VARCHAR(20) UNIQUE NOT NULL,
    user_id INT UNIQUE NOT NULL
);

-- Table for Enrollments
CREATE TABLE core_enrollment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_of_study INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    date_enrolled DATETIME DEFAULT CURRENT_TIMESTAMP,
    course_id INT NOT NULL,
    student_id INT NOT NULL
);

-- Table for Marks
CREATE TABLE core_subjectmark (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marks INT DEFAULT 0,
    enrollment_id INT NOT NULL,
    subject_id INT NOT NULL
);
