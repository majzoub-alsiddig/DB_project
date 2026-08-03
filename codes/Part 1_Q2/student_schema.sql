-- ============================================================
--  STUDENT DATABASE — Part 1, Q2 practice (Figure 2)
-- ============================================================

CREATE TABLE IF NOT EXISTS STUDENT (
    Name           TEXT,
    Student_number INTEGER PRIMARY KEY,
    Class          INTEGER,
    Major          TEXT
);

CREATE TABLE IF NOT EXISTS COURSE (
    Course_name   TEXT,
    Course_number TEXT PRIMARY KEY,
    Credit_hours  INTEGER,
    Department    TEXT
);

CREATE TABLE IF NOT EXISTS SECTION (
    Section_identifier INTEGER PRIMARY KEY,
    Course_number       TEXT,
    Semester            TEXT,
    Year                INTEGER,
    Instructor          TEXT
);

CREATE TABLE IF NOT EXISTS GRADE_REPORT (
    Student_number     INTEGER,
    Section_identifier INTEGER,
    Grade              TEXT,
    PRIMARY KEY (Student_number, Section_identifier)
);

CREATE TABLE IF NOT EXISTS PREREQUISITE (
    Course_number       TEXT,
    Prerequisite_number TEXT,
    PRIMARY KEY (Course_number, Prerequisite_number)
);

-- ------------------------------------------------------------
-- بيانات Figure 2
-- ------------------------------------------------------------

INSERT INTO STUDENT VALUES
('Smith', 17, 1, 'CS'),
('Brown', 8, 2, 'CS');

INSERT INTO COURSE VALUES
('Intro to Computer Science', 'CS1310', 4, 'CS'),
('Data Structures', 'CS3320', 4, 'CS'),
('Discrete Mathematics', 'MATH2410', 3, 'MATH'),
('Database', 'CS3380', 3, 'CS');

INSERT INTO SECTION VALUES
(85, 'MATH2410', 'Fall', 2007, 'King'),
(92, 'CS1310', 'Fall', 2007, 'Anderson'),
(102, 'CS3320', 'Spring', 2008, 'Knuth'),
(112, 'MATH2410', 'Fall', 2008, 'Chang'),
(119, 'CS1310', 'Fall', 2008, 'Anderson'),
(135, 'CS3380', 'Fall', 2008, 'Stone');

INSERT INTO GRADE_REPORT VALUES
(17, 112, 'B'),
(17, 119, 'C'),
(8, 85, 'A'),
(8, 92, 'A'),
(8, 102, 'B'),
(8, 135, 'A');

INSERT INTO PREREQUISITE VALUES
('CS3380', 'CS3320'),
('CS3380', 'MATH2410'),
('CS3320', 'CS1310');
