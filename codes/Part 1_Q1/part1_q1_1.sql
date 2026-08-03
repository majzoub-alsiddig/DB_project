/* 
a. For each department whose average employee salary is more than $30,000, 
retrieve the department name and the number of employees working for that 
department.
*/

SELECT D.Dname, COUNT(*) AS Num_Employees
FROM DEPARTMENT D, EMPLOYEE E
WHERE D.Dnumber = E.Dno
GROUP BY D.Dname
HAVING AVG(E.Salary) > 30000;


/* 
b. Suppose that we want the number of male employees in each department 
making more than $30,000, rather than all employees. Can we specify this 
query in SQL? Why or why not? 
 */

SELECT D.Dname, COUNT(*) AS Num_Male_Employees
FROM DEPARTMENT D, EMPLOYEE E
WHERE D.Dnumber = E.Dno
  AND E.Sex = 'M'
  AND E.Salary > 30000
GROUP BY D.Dname;


/* 
Yes, we can specify this query in SQL. Since the conditions "male" and "salary
 greater than $30,000"
 apply to each employee individually rather than to an aggregated group value,
 they are placed in the WHERE clause
 */
