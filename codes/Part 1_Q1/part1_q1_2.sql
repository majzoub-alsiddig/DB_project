-- ============================================================
--  Q1.2 — الـ View: DEPT_SUMMARY
-- ============================================================

CREATE VIEW DEPT_SUMMARY (D, C, Total_s, Average_s) AS
SELECT Dno, COUNT(*), SUM(Salary), AVG(Salary)
FROM EMPLOYEE
GROUP BY Dno;

/* 
(a) SELECT * FROM DEPT_SUMMARY;
Allowed?  Yes — any regular SELECT on a View is always allowed
 */

SELECT * FROM DEPT_SUMMARY;

/* 
 Result:
  (1, 1, 55000, 55000)     Headquarters
 (4, 3, 93000, 31000)      Administration
 (5, 4, 133000, 33250)     Research
 */

/* 
 (b) SELECT D, C FROM DEPT_SUMMARY WHERE TOTAL_S > 100000;

 Allowed?  Yes
 */
SELECT D, C FROM DEPT_SUMMARY WHERE Total_s > 100000;

/* 
Result: (5, 4)   -- only the Research department has total salary > 100000
 */

/* 

 (c) SELECT D, AVERAGE_S FROM DEPT_SUMMARY
      WHERE C > (SELECT C FROM DEPT_SUMMARY WHERE D = 4);
 Allowed?  Yes — still a regular SELECT, even with a subquery.
 The "View is not updatable" rule only applies to
 UPDATE/DELETE, not to SELECT of any complexity.

 */
SELECT D, Average_s FROM DEPT_SUMMARY
WHERE C > (SELECT C FROM DEPT_SUMMARY WHERE D = 4);

/* 
Result: (5, 33250.0)  
 */

/* 
(d) UPDATE DEPT_SUMMARY SET D = 3 WHERE D = 4;

 Allowed?  No
 Reason: The View contains a GROUP BY and aggregate functions
 (COUNT, SUM, AVG). There are no real EMPLOYEE rows that SQLite
 can "translate" an UPDATE on these computed values into,
so the view is not updatable.


 UPDATE DEPT_SUMMARY SET D = 3 WHERE D = 4;
 Result:
 Error: cannot modify DEPT_SUMMARY because it is a view

 */

/* 

 (e) DELETE FROM DEPT_SUMMARY WHERE C > 4;

 Allowed?  No , exact same reason as (d)

 DELETE FROM DEPT_SUMMARY WHERE C > 4;
 Result
 Error: cannot modify DEPT_SUMMARY because it is a view

 */