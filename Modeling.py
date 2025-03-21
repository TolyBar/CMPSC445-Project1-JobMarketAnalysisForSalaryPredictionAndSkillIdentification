import numpy as np
import sns
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import seaborn as sns

# Load the data
df = pd.read_csv('preprocessed_jobs.csv')

# Initialize OneHotEncoder without 'sparse' argument (since it's the default now)
encoder = OneHotEncoder(sparse_output=False)

# Apply One-Hot Encoding to the 'Title' column and drop the original 'Title' column
title_encoded = encoder.fit_transform(df[['Job Title']])
title_encoded_df = pd.DataFrame(title_encoded, columns=encoder.get_feature_names_out(['Job Title']))
df = pd.concat([df, title_encoded_df], axis=1)

# Apply One-Hot Encoding to the 'Location' column
location_encoded = encoder.fit_transform(df[['Location']])
location_encoded_df = pd.DataFrame(location_encoded, columns=encoder.get_feature_names_out(['Location']))
df = pd.concat([df, location_encoded_df], axis=1)

# Apply One-Hot Encoding to the 'Company' column
company_encoded = encoder.fit_transform(df[['Company']])
company_encoded_df = pd.DataFrame(company_encoded, columns=encoder.get_feature_names_out(['Company']))
df = pd.concat([df, company_encoded_df], axis=1)

# Drop the original categorical columns
df.drop(columns=['Job Title'], inplace=True)
df.drop(columns=['Location'], inplace=True)
df.drop(columns=['Company'], inplace=True)
df.drop(columns=['Description'], inplace=True)

# Transform Salary (since it's a continuous variable, but we'll scale it into small chunks)
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

# Save engineered data
df.to_csv("last_jobs_data.csv", index=False)

# Calculate and print correlation matrix
corr_matrix = df.corr()
target_corr = corr_matrix['Salary'].sort_values(ascending=False)
print(target_corr)

# Define the selected features based on correlation
selected_features = ['Company_Small', 'Management', 'Programming', 'Job Title_Software Engineer', 'Location_West']

# Prepare the data
X = df[selected_features]
y = df['Salary']

# Encode target variable
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Salary Prediction : Model-1 (Linear Regression Model)
# Initialize and train the Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Make predictions
y_pred_lr = lr_model.predict(X_test)

# Evaluate Linear Regression Model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

print(f'Linear Regression - Mean Squared Error: {mse_lr}')
print(f'Linear Regression - R-squared: {r2_lr}')

# Salary Prediction : Model-2 (XGBoost Model)
# Initialize and train the XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', eval_metric='rmse', max_depth=3, eta=0.1, n_estimators=100)
xgb_model.fit(X_train, y_train)

# Make predictions
y_pred_xgb = xgb_model.predict(X_test)

# Evaluate XGBoost Model
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
r2_xgb = r2_score(y_test, y_pred_xgb)

print(f'XGBoost - Mean Squared Error: {mse_xgb}')
print(f'XGBoost - R-squared: {r2_xgb}')


# Plot for Linear Regression Model 
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_lr, color='blue', edgecolor='k', alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')  # Line of perfect prediction
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.title('Linear Regression Model for Features')
plt.show()

# Plot for XGBoost Model 
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_xgb, color='green', edgecolor='k', alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')  # Line of perfect prediction
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.title('XGBoost Model for Features')
plt.show()

X = df[['Management', 'Programming', 'Communication']]  # Features

# The target is the one-hot encoded columns of the Titles
title_columns = [col for col in df.columns if col.startswith('Job Title_')]  # Get all columns starting with 'Job Title_'
y = df[title_columns].values  # Get the one-hot encoded target columns

# Convert the one-hot encoded target into integer labels (class indices)
y_encoded = np.argmax(y, axis=1)

# Get the number of classes (unique titles)
num_classes = len(title_columns)  # The number of distinct classes (titles)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train XGBoost Model
xgb_model = xgb.XGBClassifier(importance_type='gain',objective='multi:softmax', eval_metric='mlogloss', num_class=num_classes, max_depth=3,
                              eta=0.1, n_estimators=100)
xgb_model.fit(X_train, y_train)

# Train Random Forest Model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Get feature importances from the XGBoost model
xgb_feature_importance = xgb_model.feature_importances_

# Get feature importances from the Random Forest model
rf_feature_importance = rf_model.feature_importances_

# Plotting the Feature Importances for Each Job Title 
# Plot for XGBoost Feature Importance 
plt.figure(figsize=(10, 6))
plt.barh(['Management', 'Programming', 'Communication'], xgb_feature_importance, color='orange')
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance for Predicting Job Titles')
plt.show()

# Plot for Random Forest Feature Importance 
plt.figure(figsize=(10, 6))
plt.barh(['Management', 'Programming', 'Communication'], rf_feature_importance, color='teal')
plt.xlabel('Feature Importance')
plt.title('Random Forest Feature Importance for Predicting Job Titles')
plt.show()

# Feature Importance Per Job Title
# For XGBoost: Plot feature importances for each job title (class)
for idx, title in enumerate(title_columns):
    # Extract feature importances for the current job title
    xgb_class_importance = xgb_model.feature_importances_

    # Create a DataFrame for better visualization
    importance_df_xgb = pd.DataFrame({
        'Skill': ['Management', 'Programming', 'Communication'],
        'Importance': xgb_class_importance
    })

    # Sort the DataFrame by importance
    importance_df_xgb = importance_df_xgb.sort_values(by='Importance', ascending=False)

    # Plot the importance for this class
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Skill', data=importance_df_xgb, color='purple')
    plt.xlabel('Feature Importance')
    plt.ylabel('Skill')
    plt.title(f'XGBoost Feature Importance for Predicting: {title}')
    plt.show()

    print(f"\nXGBoost Feature Importances for {title}:")
    for feature, importance in zip(['Management', 'Programming', 'Communication'], xgb_class_importance):
        print(f"{feature}: {importance}")

# For Random Forest: Plot feature importances for each job title (class)
for idx, title in enumerate(title_columns):
    # Extract feature importances for the current job title
    rf_class_importance = rf_model.feature_importances_

    # Create a DataFrame for better visualization
    importance_df_rf = pd.DataFrame({
        'Skill': ['Management', 'Programming', 'Communication'],
        'Importance': rf_class_importance
    })

    # Sort the DataFrame by importance
    importance_df_rf = importance_df_rf.sort_values(by='Importance', ascending=False)

    # Plot the importance for this class
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Skill', data=importance_df_rf, color='green')
    plt.xlabel('Feature Importance')
    plt.ylabel('Skill')
    plt.title(f'Random Forest Feature Importance for Predicting: {title}')
    plt.show()

    print(f"\nRandom Forest Feature Importances for {title}:")
    for feature, importance in zip(['Management', 'Programming', 'Communication'], rf_class_importance):
        print(f"{feature}: {importance}")

# Get predictions for the job roles (encoded columns)
y_pred_job_roles = xgb_model.predict(X_test)

# Reverse label encoding (if necessary, because the target is encoded)
y_pred_job_roles = le.inverse_transform(y_pred_job_roles)

# Create a DataFrame with the actual and predicted job roles 
predictions_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred_job_roles
})

# Add predicted salaries (from the XGBoost model) to the DataFrame
predictions_df['Predicted_Salary'] = y_pred_xgb  # Using the predicted salary from the XGBoost regression model

# Get the one-hot encoded job title columns 
title_columns = [col for col in df.columns if col.startswith('Title_')]

# Plot histograms for each job title
for title_col in title_columns:
    # Filter the data for the specific job title (where the one-hot column is 1)
    role_data = predictions_df[predictions_df['Predicted'] == title_col]

    # Plot histogram of predicted salaries for the job role
    plt.figure(figsize=(8, 6))
    plt.hist(role_data['Predicted_Salary'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Predicted Salary')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Predicted Salaries for {title_col}')
    plt.show()

# Reverse label encoding for y_test to get the original job role names
y_test_reversed = le.inverse_transform(y_test)
# Prepare the DataFrame with actual job roles and predicted salaries
predictions_df['Actual_Job_Role'] = y_test_reversed  # Assign actual job roles to DataFrame

# If 'Location' is one-hot encoded, you need to reverse it back to the original categorical form.
location_columns = [col for col in df.columns if col.startswith('Location_')]
predictions_df['Location'] = df.loc[X_test.index, location_columns].idxmax(axis=1).str.replace('Location_', '')

# Box Plot for Job Roles vs. Predicted Salaries, grouped by Location
plt.figure(figsize=(12, 8))
sns.boxplot(
    x='Actual_Job_Role', 
    y='Predicted_Salary', 
    hue='Location',  # Group by Location
    data=predictions_df, 
    palette="Set2", 
    legend=True
)
plt.title('Salary Distribution Across Different Job Roles and Locations')
plt.xlabel('Job Role')
plt.ylabel('Predicted Salary')
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better visibility
plt.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')  # Move legend outside the plot
plt.tight_layout()  # Adjust layout to prevent overlapping
plt.show()

# Feature importance extraction from XGBoost model  
xgb_feature_importances = xgb_model.feature_importances_

# Feature importance extraction from Random Forest model 
rf_feature_importances = rf_model.feature_importances_

# Define skills (features)
skills = ['Management', 'Programming', 'Communication']

# Create a DataFrame to hold feature importances for each model
importance_df = pd.DataFrame({
    'Skill': skills,
    'XGBoost': xgb_feature_importances,
    'Random Forest': rf_feature_importances
})

# Set the index to be the 'Skill' column for better heatmap visualization 
importance_df.set_index('Skill', inplace=True)

# Plot heatmap for feature importances
plt.figure(figsize=(8, 6))
sns.heatmap(importance_df.T, annot=True, cmap='coolwarm', cbar=True, fmt='.4f', linewidths=0.5)
plt.title('Feature Importance for Job Titles (XGBoost & Random Forest)')
plt.xlabel('Skill')
plt.ylabel('Model')
plt.show()
