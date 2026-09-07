
-- Employee Segmentation Analysis SQL Queries

-- 1. Segment Distribution
SELECT
    Segment,
    COUNT(*) as Employee_Count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as Percentage
FROM employee_segmentation
GROUP BY Segment
ORDER BY Employee_Count DESC;

-- 2. Department Performance by Segment
SELECT
    Department,
    Segment,
    COUNT(*) as Employee_Count,
    AVG(Annual_Salary) as Avg_Salary,
    AVG(Performance_Rating) as Avg_Performance,
    AVG(Employee_Satisfaction) as Avg_Engagement
FROM employee_segmentation
GROUP BY Department, Segment
ORDER BY Department, Segment;

-- 3. Attrition Risk Segments
SELECT
    Segment,
    ROUND(AVG(Attrition) * 100, 1) as Attrition_Rate,
    ROUND(AVG(Employee_Satisfaction), 2) as Avg_Engagement,
    ROUND(AVG(Overtime_Hours), 1) as Avg_Overtime,
    ROUND(AVG(Absenteeism_Days), 1) as Avg_Absenteeism
FROM employee_segmentation
GROUP BY Segment
ORDER BY Attrition_Rate DESC;

-- 4. High Performers Analysis
SELECT
    Department,
    COUNT(*) as High_Performers,
    ROUND(AVG(Annual_Salary), 0) as Avg_Salary,
    ROUND(AVG(Company_Tenure), 1) as Avg_Tenure
FROM employee_segmentation
WHERE Segment = 'High Performers'
GROUP BY Department
ORDER BY High_Performers DESC;

-- 5. HR Intervention Priority
SELECT
    Segment,
    COUNT(*) as At_Risk_Employees,
    ROUND(AVG(Attrition) * 100, 1) as Attrition_Rate,
    ROUND(AVG(Employee_Satisfaction), 2) as Engagement_Level,
    ROUND(AVG(Performance_Rating), 2) as Performance_Level
FROM employee_segmentation
WHERE Segment IN ('Retention Risk', 'Disengaged Employees', 'Needs Improvement')
GROUP BY Segment
ORDER BY Attrition_Rate DESC;
