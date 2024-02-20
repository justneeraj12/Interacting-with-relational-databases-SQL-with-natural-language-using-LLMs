CREATE TABLE Department (
  Dept_id INT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL
);

CREATE TABLE Class (
  Class_id INT PRIMARY KEY,
  Course_id INT NOT NULL,
  Section VARCHAR(255) NOT NULL,
  Semester VARCHAR(255) NOT NULL,
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)
);

CREATE TABLE Teacher (
  Teacher_id INT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  DOB DATE NOT NULL,
  Sex VARCHAR(10) NOT NULL
);

CREATE TABLE Course (
  Course_id INT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Dept_id INT NOT NULL,
  Shortname VARCHAR(255) NOT NULL,
  FOREIGN KEY (Dept_id) REFERENCES Department(Dept_id)
);

CREATE TABLE Student (
  USN VARCHAR(255) PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  DOB DATE NOT NULL,
  Sex VARCHAR(10) NOT NULL
);

CREATE TABLE Student_Course (
  USN VARCHAR(255) NOT NULL,
  Course_id INT NOT NULL,
  Marks INT,
  Attendance VARCHAR(255),
  Status VARCHAR(255),
  PRIMARY KEY (USN, Course_id),
  FOREIGN KEY (USN) REFERENCES Student(USN),
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)
);

CREATE TABLE Assign (
  Assign_id INT PRIMARY KEY,
  USN VARCHAR(255) NOT NULL,
  Class_id INT NOT NULL,
  Teacher_id INT NOT NULL,
  Day VARCHAR(255) NOT NULL,
  Time_Slot VARCHAR(255) NOT NULL,
  Assign_Time TIME NOT NULL,
  FOREIGN KEY (USN) REFERENCES Student(USN),
  FOREIGN KEY (Class_id) REFERENCES Class(Class_id),
  FOREIGN KEY (Teacher_id) REFERENCES Teacher(Teacher_id)
);

CREATE TABLE Test (
  Test_id INT PRIMARY KEY,
  Course_id INT NOT NULL,
  Date DATE NOT NULL,
  Total_marks INT NOT NULL,
  FOREIGN KEY (Course_id) REFERENCES Course(Course_id)
);
