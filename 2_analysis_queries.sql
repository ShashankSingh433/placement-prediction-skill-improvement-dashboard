-- 1. Placement rate by branch
SELECT 
    Branch,
    COUNT(*) AS Total_Students,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS Placed_Students,
    ROUND((SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS Placement_Rate
FROM cleaned_students
GROUP BY Branch
ORDER BY Placement_Rate DESC;

-- 2. Average CGPA of placed vs non-placed students
SELECT 
    Placement_Status,
    ROUND(AVG(CGPA), 2) AS Average_CGPA
FROM cleaned_students
GROUP BY Placement_Status;

-- 3. Internship count vs placement rate
SELECT 
    Internship_Count,
    COUNT(*) AS Total_Students,
    ROUND((SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS Placement_Rate
FROM cleaned_students
GROUP BY Internship_Count
ORDER BY Internship_Count ASC;

-- 4. Top 5 factors affecting placement (Approximate correlation view)
SELECT 
    Placement_Status,
    ROUND(AVG(Coding_Score), 2) AS Avg_Coding,
    ROUND(AVG(Communication_Score), 2) AS Avg_Communication,
    ROUND(AVG(Aptitude_Score), 2) AS Avg_Aptitude,
    ROUND(AVG(Internship_Count), 2) AS Avg_Internships,
    ROUND(AVG(Backlogs), 2) AS Avg_Backlogs
FROM cleaned_students
GROUP BY Placement_Status;

-- 5. Average package by branch and company type
SELECT 
    Branch,
    Company_Type,
    ROUND(AVG(Package_Offered), 2) AS Average_Package
FROM cleaned_students
WHERE Placement_Status = 'Placed'
GROUP BY Branch, Company_Type
ORDER BY Branch, Average_Package DESC;
