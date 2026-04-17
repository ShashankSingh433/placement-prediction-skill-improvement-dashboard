-- 1. Remove Duplicates (Assuming a staging table exists)
-- CREATE TABLE cleaned_students AS
-- SELECT DISTINCT *
-- FROM raw_students;

-- 2. Handle Missing Values
-- Set default values for missing numerical scores (conceptual mapping)
-- UPDATE cleaned_students
-- SET Aptitude_Score = (SELECT AVG(Aptitude_Score) FROM cleaned_students WHERE Aptitude_Score IS NOT NULL)
-- WHERE Aptitude_Score IS NULL;

-- 3. Standardize Branch Names
-- UPDATE cleaned_students
-- SET Branch = UPPER(TRIM(Branch));

-- 4. Clean Company Types
-- UPDATE cleaned_students
-- SET Company_Type = 'None'
-- WHERE Placement_Status = 'Not Placed' AND Company_Type IS NULL;

-- 5. Standardize Packages
-- UPDATE cleaned_students
-- SET Package_Offered = 0.0
-- WHERE Placement_Status = 'Not Placed';

-- Check final distinct branches
-- SELECT DISTINCT Branch FROM cleaned_students;
