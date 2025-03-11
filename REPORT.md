# CMPSC445-Project1-JobMarketAnalysisForSalaryPredictionAndSkillIdentification

#  Description of the Project
This project aims to analyze job listings to identify the most important skills required for various job roles in computer science, data science, and AI. It involves data collection through web scraping, data preprocessing, feature engineering, model development, and visualization to provide insights into job market trends and skill requirements.

#  How to Use/Setup
Note: For first time use must uncomment the webscraper portion.
Clone the Repository:

    git clone https://github.com/your_username/job-market-analysis.git
    cd job-market-analysis
Install Dependencies and Uncomment Webscraper portion if neccessary.
Run the Preprocessing and Analysis:

    pip install numpy pandas scikit-learn xgboost matplotlib seaborn selenium
    python Scraper.py
#  Training
            1. Data Collection:

* Tools Used:

The job data was collected using Selenium WebDriver with ChromeDriver for automated web scraping.
Pandas was used for storing and exporting the extracted data into a CSV file.

* Data Sources:

The script scrapes job postings from Glassdoor and SimplyHired.

* Collected Attributes:

Job Title

Company Name

Location (State or Remote)

Salary (if provided)

Required Skills (if available)

Job Description Snippet

* Number of Data Samples:

The script loads and extracts up to 800 job postings per search query.
It targets multiple states, covering job postings from New York, California, Florida, Massachusetts, Maryland, Oregon, and Washington.
The total number of job samples collected can reach several thousand depending on availability.

    Process Overview

The script navigates to the target job listing pages.
It clicks the "Load More" button multiple times to fetch more job postings.
It extracts relevant job information using XPath and CSS selectors.
It processes location data to extract state abbreviations or identify remote jobs.
The collected data is saved to a CSV file in an append mode, ensuring incremental data storage.

            2. Data Preprocessing:
* Loading the Data and Handling Missing Values:

Loading the dataset from a CSV file named jobs.csv using pandas.

Filling missing values in the Salary and Skills columns with "N/A" to ensure that no empty cells would cause issues during processing.

* Standardizing Job Titles:

Cleaning and standardizing the Job Title column by:

Removing extra descriptions using regex.

Stripping leading and trailing spaces.

Removing single and double quotes.

Applieing a function standardize_title to categorize job titles into broader categories such as "Artificial Intelligence", "Software Engineer", "Software Developer", and "Other" based on specific keywords.

* Standardizing Skills:

Standardizing variations in the Skills column, such as replacing "Dev-Ops" with "DevOps" and "C Plus Plus" with "C++".

* Standardizing Locations:

You standardized the Location column by replacing variations of state names (e.g., "New York" to "NY") and categorizing locations into broader regions like "East" and "West" based on specific state codes (e.g., NY, WA, CA, etc.).

* Standardizing Company Size:

Categorizing companies into "Large" or "Small" based on a predefined list of large companies (e.g., Google, Microsoft, etc.).

* Handling Salary Data:

Creating a function calculate_mean_salary to process the Salary column:

Handling different salary formats, including hourly wages and yearly salary ranges.

Converting hourly wages to yearly salaries by assuming a standard work schedule (40 hours/week * 52 weeks/year).

Calculating the mean salary for ranges (e.g., "87K−91K") and converted them to integers.

Removiong rows with missing or non-numeric salary values after processing.

* Extracting Salary Information:

Spliting the Skills column into a list of individual skills and categorized them into three new binary features: Communication, Programming, and Management.

Dropping the original Skills column after extracting these features.

            3. Feature Engineering:
    
* Creating New Features:

    * Creating new features such as:

        Job Title: Standardized job titles into broader categories.

        Company Size: Categorized companies into "Large" or "Small".

        Location: Standardized locations into broader regions (e.g., "East", "West").

        Required Skills: Extracted and categorized skills into Communication, Programming, and Management features.

* Saving the Preprocessed Data:

    Saving the cleaned and preprocessed data to a new CSV file named preprocessed_jobs.csv without the index column.

        
            4. Model Development and Evaluation:
* Salary Prediction:

Training two different machine learning models to predict salaries based on the extracted features from the preprocessed job data.

* Train and Test Data Partition:
  
The dataset was split into training (80%) and testing (20%) sets using train_test_split from sklearn.model_selection.

The features (X) included:

 - Company_Small

 - Management

 - Programming

 - Job Title_Software Engineer

 - Location_West

The target variable (y) was the Salary column.

    !Salary Prediction: Model-1 (Linear Regression)!
Machine Learning Model: Linear Regression (LinearRegression from sklearn.linear_model).

Input to Model: Scaled features (X_scaled) and encoded target (y_encoded).

Size of Train Data: 80% of the dataset.

Attributes to the Model:

* Features: Company_Small, Management, Programming, Job Title_Software Engineer, Location_West.

* Target: Salary (encoded).

Performance with Training Data: Not explicitly calculated in the script.

Performance with Test Data:

* Mean Squared Error (MSE): Calculated using mean_squared_error.

* R-squared (R²): Calculated using r2_score.

* Results:

    * Linear Regression - Mean Squared Error: [Value]

    *Linear Regression - R-squared: [Value]

        !Salary Prediction: Model-2 (XGBoost)!
Machine Learning Model: XGBoost Regressor (XGBRegressor from xgboost).

Input to Model: Scaled features (X_scaled) and encoded target (y_encoded).

Size of Train Data: 80% of the dataset.

Attributes to the Model:

* Features: Company_Small, Management, Programming, Job Title_Software Engineer, Location_West.

* Target: Salary (encoded).

* Hyperparameters: max_depth=3, eta=0.1, n_estimators=100.

Performance with Training Data: Not explicitly calculated in the script.

Performance with Test Data:

* Mean Squared Error (MSE): Calculated using mean_squared_error.

* R-squared (R²): Calculated using r2_score.

* Results:

    * XGBoost - Mean Squared Error: [Value]

    * XGBoost - R-squared: [Value]

            Skill Importance:
Description of Feature Importance Techniques:

* XGBoost Feature Importance: The feature_importances_ attribute of the XGBoost model was used to extract the importance of each feature (skill) for predicting job titles.

* Random Forest Feature Importance: The feature_importances_ attribute of the RandomForestClassifier was used to extract the importance of each feature (skill) for predicting job titles.

Identified Important Skills for All Job Roles:

* Calculating feature importance for all job titles (e.g., Job Title_Software Engineer, Job Title_Artificial Intelligence, etc.).

* The important skills identified were:

    * Management

    * Programming

    * Communication

              5. Visualization
Model 1:

![Figure_1](https://github.com/user-attachments/assets/b693e0df-575b-4210-a480-1a267fd62d93)

Model 2:

![Figure_2](https://github.com/user-attachments/assets/a3710bce-fa28-41ea-a29a-f99c98046219)

Predicted Salaries and Salary Distribution:

* Histograms:

![Figure_3](https://github.com/user-attachments/assets/a728debb-d665-4f48-a9fc-7b1e171c038a)

![Figure_4](https://github.com/user-attachments/assets/2ab8fbb7-61fa-4321-8df2-6c7c6afb03cc)

Histograms were plotted to show the distribution of predicted salaries for different job roles (e.g., Job Title_Software Engineer, Job Title_Artificial Intelligence, etc.).

* Box Plots:

![Figure_5](https://github.com/user-attachments/assets/e1c01d29-b4e6-46a8-a2c7-7c3dcac37068)

![Figure_6](https://github.com/user-attachments/assets/6dde1619-ddfc-400e-a76a-ed5b66bdd5f4)

![Figure_7](https://github.com/user-attachments/assets/b2f52db6-7e36-41f1-ad22-14f04b09f7b2)

![Figure_8](https://github.com/user-attachments/assets/dfe132fb-a621-454b-a458-eb475b9671e5)

![Figure_9](https://github.com/user-attachments/assets/47702a15-e610-42df-a40f-391ea4895743)

![Figure_10](https://github.com/user-attachments/assets/cc24f362-b048-4bf3-9aad-9af3c11d3a8d)

![Figure_11](https://github.com/user-attachments/assets/ef290517-ce99-4ef0-a808-e1e4c472a9be)

![Figure_12](https://github.com/user-attachments/assets/182e981f-69b8-48e2-a27d-1a2ecf9204a7)

Box plots were created to compare the salary distributions across different job roles and locations.

2. Skill Importance Visualization:

* Bar Plots:

![Figure_13](https://github.com/user-attachments/assets/f4af0dd4-541d-46d3-b550-a62f5a12922d)

Bar plots were used to show the importance of different skills (e.g., Management, Programming, Communication) for each job role.

* Heatmaps:

![Figure_14](https://github.com/user-attachments/assets/00c00fb5-9961-4140-a4c9-2425d12bb282)

Heatmaps were created to visualize the importance of skills across different job roles.



#  Discussion and Conclusions
   

