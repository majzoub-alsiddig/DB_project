/*
  Q2 (a) — Straight-A students
 Retrieve the names and major departments of all
  straight-A students (students who have a grade of A
  in ALL their courses).
 */


SELECT S.Name, S.Major
FROM STUDENT S
WHERE NOT EXISTS (
    SELECT *
    FROM GRADE_REPORT G
    WHERE G.Student_number = S.Student_number
    AND G.Grade <> 'A'
);

/*
 Result: (empty — no rows)
 Smith has a B and a C (no A at all), Brown has three A's but also
one B.
 */ 
