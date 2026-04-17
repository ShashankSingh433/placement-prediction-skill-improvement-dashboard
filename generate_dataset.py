import pandas as pd
import random
import numpy as np
import os

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_data(n=250):
    branches = ['CS', 'IT', 'ECE', 'Mech', 'Civil']
    data = []
    
    for i in range(1, n + 1):
        name = f"Student_{i}"
        branch = random.choice(branches)
        
        # Base attributes
        cgpa = round(random.uniform(6.0, 9.8), 2)
        apt = random.randint(40, 95)
        comm = random.randint(40, 95)
        
        # Branch specific bias
        if branch in ['CS', 'IT']:
            coding = random.randint(60, 98)
        else:
            coding = random.randint(30, 85)
            
        internships = random.randint(0, 3)
        projects = random.randint(0, 5)
        backlogs = random.randint(0, 3)
        
        # Probability calculation
        score = (cgpa * 10) + (apt * 0.2) + (comm * 0.2) + (coding * 0.3) + (internships * 5) - (backlogs * 15)
        
        if score > 120 and backlogs <= 1:
            placed = 'Placed'
            if coding > 80 and cgpa > 8.0:
                company = 'Product'
                package = round(random.uniform(10.0, 25.0), 2)
            else:
                company = 'Service'
                package = round(random.uniform(3.5, 9.0), 2)
        else:
            placed = 'Not Placed'
            company = 'None'
            package = 0.0
            
        data.append([i, name, branch, cgpa, apt, comm, coding, internships, projects, backlogs, placed, company, package])

    df = pd.DataFrame(data, columns=[
        'Student_ID', 'Name', 'Branch', 'CGPA', 'Aptitude_Score', 
        'Communication_Score', 'Coding_Score', 'Internship_Count', 
        'Project_Count', 'Backlogs', 'Placement_Status', 
        'Company_Type', 'Package_Offered'
    ])
    
    os.makedirs('../dataset', exist_ok=True)
    df.to_csv('../dataset/placement_dataset.csv', index=False)
    print("Dataset generated successfully at ../dataset/placement_dataset.csv")

if __name__ == "__main__":
    generate_data(250)
