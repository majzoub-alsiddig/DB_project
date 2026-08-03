/* 
 Q2 (b) — Students with no A grade at all
 Retrieve the names and major departments of all
 students who do NOT have a grade of A in ANY of
 their courses.
 */



SELECT S.Name, S.Major
FROM STUDENT S
WHERE NOT EXISTS (
    SELECT *
    FROM GRADE_REPORT G
    WHERE G.Student_number = S.Student_number
    AND G.Grade = 'A'
);
/* 
 Result:
 Smith, CS (Smith's grades are B and C , no A at all)
 */

