# Power BI Dashboard Layout & Implementation Guide

## Theme & Design Requirements
- **Theme**: Modern Dark-Blue (#0B192C) + Cyan (#00E5FF) Accents
- **Style**: Corporate analytics style with rounded cards, subtle shadows, and a recruiter-friendly clean spacing.

## Data Import
1. Load `placement_dataset.csv` into Power BI.
2. (Optional) Run Python scripts internally inside Power BI using "Get Data -> Python Script" to natively import predictions from `skill_engine.py`.

## Global Filters (Slicers on Left Panel)
- **Branch** (Dropdown: CS, IT, ECE, Mech, Civil)
- **Company Type** (Dropdown: Product, Service, None)
- **Placement Status** (Radio: Placed, Not Placed)

## Top Section: KPI Cards
1. **Total Students**: `COUNT(Student_ID)`
2. **Placement Rate**: `% Placed = DIVIDE(CALCULATE(COUNTROWS(Table), Table[Placement_Status]="Placed"), COUNTROWS(Table))`
3. **Highest Placement Branch**: Visual showing Top 1 Branch by Placement Rate.
4. **Students At Risk**: `COUNTROWS(FILTER(Table, Table[CGPA] < 6.5 || Table[Backlogs] > 1))` (Use red warning icon mask).

## Middle Section: Primary Charts
1. **Placement by Branch (Bar Chart)**: 
   - X-Axis: Branch
   - Y-Axis: Placement Rate (%)
   - Color: Cyan
2. **CGPA vs Placement (Box Plot / Scatter)**:
   - X-Axis: CGPA
   - Y-Axis: Placed / Not Placed
3. **Package Distribution (Histogram)**:
   - Values: Package_Offered (LPA)
   - Filtered for `Placement_Status = 'Placed'`

## Bottom Section: "What Should Improve?" (Skill Improvement Engine)
Create a **Matrix/Table Visual** mapped to the output of `skill_engine.py` (which generates recommendations row-by-row):
- **Columns**: Student Name | Weakest Skill | Recommendation | Prob Before | Prob After
- **Conditional Formatting**: Highlight *Prob After* in green if it increases by > 15%.
