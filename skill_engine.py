import pandas as pd
import pickle
import numpy as np

# Load Model
try:
    with open('model.pkl', 'rb') as f:
        saved_data = pickle.load(f)
        model = saved_data['model']
        le_branch = saved_data['le_branch']
        features = saved_data['features']
except FileNotFoundError:
    print("Model file not found. Ensure eda_and_models.py runs first.")
    exit(1)

def calculate_probability(student_data):
    # Predict probabilities requires dataframe matching training features
    df_temp = pd.DataFrame([student_data])
    df_temp['Branch_Encoded'] = le_branch.transform([df_temp['Branch'][0]])[0]
    X_input = df_temp[features]
    prob = model.predict_proba(X_input)[0][1] # Probability of Class 1 (Placed)
    return round(prob * 100, 2)

def generate_recommendation(student_row):
    current_prob = calculate_probability(student_row)
    
    # Identify Weakest Skill
    # Our core metrics are Communication, Coding, and Internships
    skills = {
        'Communication_Score': student_row['Communication_Score'],
        'Coding_Score': student_row['Coding_Score']
    }
    
    weakest_skill = min(skills, key=skills.get)
    weakest_value = skills[weakest_skill]
    
    recommendation = ""
    simulated_row = student_row.copy()
    
    if student_row['Internship_Count'] == 0:
        weakest_skill = 'Internship_Count'
        recommendation = "You have 0 internships. Suggesting to complete at least 1 internship to boost profile."
        simulated_row['Internship_Count'] = 1
    elif weakest_skill == 'Communication_Score' and weakest_value < 70:
        recommendation = f"Communication score is critically low ({weakest_value}). Suggest attending mock interviews to reach 75+."
        simulated_row['Communication_Score'] = max(75, weakest_value + 15)
    elif weakest_skill == 'Coding_Score' and weakest_value < 75:
        recommendation = f"Coding score is low ({weakest_value}). Suggest practicing algorithmic problems and projects to reach 80."
        simulated_row['Coding_Score'] = max(80, weakest_value + 20)
    elif student_row['CGPA'] < 7.0:
        weakest_skill = 'CGPA'
        recommendation = f"CGPA is low ({student_row['CGPA']}). Push to improve academic scores."
        simulated_row['CGPA'] = 7.5
    else:
        recommendation = "Profile looks solid. Keep maintaining current performance."
        
    new_prob = calculate_probability(simulated_row)
    
    return {
        'Student_ID': student_row.get('Student_ID', 'N/A'),
        'Name': student_row.get('Name', 'Unknown'),
        'Current_Probability': f"{current_prob}%",
        'Weakest_Skill': weakest_skill.replace('_Score', ''),
        'Recommendation': recommendation,
        'Predicted_Probability_After': f"{new_prob}%"
    }

if __name__ == "__main__":
    # Test on all records and output to CSV
    df = pd.read_csv('../dataset/placement_dataset.csv')
    print("--- Skill Improvement Engine ---")
    results = []
    for idx, row in df.iterrows():
        res = generate_recommendation(row.to_dict())
        results.append(res)
        
    out_df = pd.DataFrame(results)
    import os
    os.makedirs('../reports', exist_ok=True)
    out_df.to_csv('../reports/prediction_output.csv', index=False)
    print("Predictions successfully saved to ../reports/prediction_output.csv")
