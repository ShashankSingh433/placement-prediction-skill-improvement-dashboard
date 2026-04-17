import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import pickle
import os

# Create directories
os.makedirs('../reports', exist_ok=True)
os.makedirs('../screenshots', exist_ok=True)

print("Loading dataset...")
df = pd.read_csv('../dataset/placement_dataset.csv')

# --- 1. Exploratory Data Analysis (EDA) ---
sns.set_theme(style="whitegrid")

# Branch-wise placement rate
plt.figure(figsize=(8, 5))
branch_placement = df.groupby('Branch')['Placement_Status'].value_counts(normalize=True).unstack()
branch_placement.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'])
plt.title('Branch-wise Placement Rate')
plt.ylabel('Proportion')
plt.savefig('../reports/branch_placement.png')
plt.close()

# CGPA vs Placement
plt.figure(figsize=(8, 5))
sns.boxplot(x='Placement_Status', y='CGPA', data=df, palette='Set2')
plt.title('CGPA vs Placement')
plt.savefig('../reports/cgpa_vs_placement.png')
plt.close()

# Coding Score vs Placement
plt.figure(figsize=(8, 5))
sns.boxplot(x='Placement_Status', y='Coding_Score', data=df, palette='Set2')
plt.title('Coding Score vs Placement')
plt.savefig('../reports/coding_vs_placement.png')
plt.close()

# Internship Count vs Package
plt.figure(figsize=(8, 5))
placed_df = df[df['Placement_Status'] == 'Placed']
sns.barplot(x='Internship_Count', y='Package_Offered', data=placed_df, palette='viridis')
plt.title('Internship Count vs Package (Placed Students)')
plt.savefig('../reports/internship_vs_package.png')
plt.close()

# Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=[np.number]).drop(columns=['Student_ID'])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Feature Correlation Heatmap')
plt.savefig('../reports/correlation_heatmap.png')
plt.close()
print("EDA plots saved to reports/ folder.")

# --- 2. Machine Learning Pipeline ---
print("Preparing data for ML...")
# Encode categorical variables
le_branch = LabelEncoder()
df['Branch_Encoded'] = le_branch.fit_transform(df['Branch'])

# Mapping Target
df['Placement_Encoded'] = df['Placement_Status'].apply(lambda x: 1 if x == 'Placed' else 0)

# Features and Target
features = ['Branch_Encoded', 'CGPA', 'Aptitude_Score', 'Communication_Score', 'Coding_Score', 'Internship_Count', 'Project_Count', 'Backlogs']
X = df[features]
y = df['Placement_Encoded']

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# We use standard scaler to normalize scores
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic Regression
lr_model = LogisticRegression()
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)

print("\n--- Logistic Regression Results ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.2f}")
print(f"Precision: {precision_score(y_test, y_pred_lr):.2f}")
print(f"Recall: {recall_score(y_test, y_pred_lr):.2f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))

# Decision Tree
dt_model = DecisionTreeClassifier(random_state=42, max_depth=5)
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)

print("\n--- Decision Tree Results ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred_dt):.2f}")
print(f"Precision: {precision_score(y_test, y_pred_dt):.2f}")
print(f"Recall: {recall_score(y_test, y_pred_dt):.2f}")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_dt))

# Feature Importance
importances = pd.Series(dt_model.feature_importances_, index=features).sort_values(ascending=False)
print("\n--- Decision Tree Feature Importance ---")
print(importances)

# Choose best model
best_model = dt_model
print("\nSaving Decision Tree model as best model...")

with open('model.pkl', 'wb') as f:
    pickle.dump({
        'model': best_model,
        'scaler': scaler,
        'le_branch': le_branch,
        'features': features
    }, f)

print("model.pkl saved successfully.")
