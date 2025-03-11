# CMPSC445-Project1-JobMarketAnalysisForSalaryPredictionAndSkillIdentification

#  Description of the Project
In this project, I was tasked with scraping various job search sites to collect data to predict salaries for specific positions based on given parameters. The project was structured into five distinct stages: data collection, data preprocessing, feature engineering, model development, and results visualization.

#  How to Use/Setup

My project requires three files. They must be used in a specific order: Scraping.py , Preprocessing.py and finally Modeling.py.

Scraping.py is a program that scrapes the specified links. Before using this program, make sure you have the necessary libraries downloaded.

To install the libraries, type in the terminal:

    pip install pandas selenium time

And also specify your path to chromedriver.exe in the line 19:

    service = Service("\\your_path\\chromedriver.exe")

After that, you can either use the code with the links I specified, or specify your own GlassDoor and SimplyHire links.

The second program in line is Preprocessing.py, which does things like: Data cleaning, Data integration, Data ingestion, Data Description, Meta data specification in the data repository with a sample data and Feature Engineering. It uses the already downloaded pandas library, so you can run the program right after the first one.

The last program Modeling.py combines the last tasks in this project, namely Model Development, Evaluation and Visualization. As for the first one, you need to install the corresponding libraries:

    pip install numpy scikit-learn xgboost matplotlib seaborn

#  Training
            1. Data Collection:

Writing Scraping.py turned out to be the most difficult task of the project, which took me several days of various tests. At first, I tried to scrape one GlassDoor link and as a result of testing I found that my code could only take ~900 jobs (may include duplicates) from any ONE link. Adding other links was not successful for a long time, until I decided to restart the driver for each link, the reason was that the site blocks the driver after refreshing the page. Thus, I managed to take from different GlassDoor urls (divided by states) ~900 jobs. And in the same way from SimplyHire.

    !Important information!

    Due to the fact that the program restarts the driver for each link, the program runtime is quite long.

And now to the specific work of the program:

One consists of functions and the main function. The functions that I wrote:
* start_driver() that starts Chrome WebDriver
* load_more_jobs(driver, target_jobs=2000) that loads more jobs
* parse_location(location_text) that parses the location text and extract the state or "Remote"
* scrape_job_element_GlassDoor(job_element) that scrapes job element from GlassDoor
* scrape_job_element_SimplyHire(job_element) that scrapes job element from SimplyHire
* scrape_jobs_GlassDoor(driver) that scrapes jobs from GlassDoor
* scrape_jobs_SimlyHire(driver) that scrapes jobs from SimplyHire
* save_to_csv(data, filename="jobs.csv") that saves data to CSV

    * Tools Used:

The job data was collected using Selenium WebDriver with ChromeDriver for automated web scraping.
Pandas was used for storing and exporting the extracted data into a CSV file.

* Data Sources:
    
The script scrapes job postings from Glassdoor and SimplyHired.

* Collected Attributes:

  * Job Title

  * Company Name

  * Location (State or Remote)

  * Salary (if provided)

  * Required Skills (if available)

  * Job Description Snippet
    
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

    * Linear Regression - Mean Squared Error: 12452.225292617819

    * Linear Regression - R-squared: 0.15779524632744535

            !Salary Prediction: Model-2 (XGBoost)!
Machine Learning Model: XGBoost Regressor (XGBRegressor from xgboost).

Input to Model: Scaled features (X_scaled) and encoded target (y_encoded).

Size of Train Data: 80% of the dataset.

Attributes to the Model:

* Features: Company_Small, Management, Programming, Job Title_Software Engineer, Location_West.

* Target: Salary (encoded).

* Hyperparameters: max_depth=3, eta=0.1, n_estimators=100.

Performance with Test Data:

Salary    1.000000

Job Title_Software Engineer    0.228669

Company_Large    0.224192

Location_West    0.191724

Location_US    0.038232

Location_SC    0.023489

Location_NJ    0.007959

Programming    0.000133

Job Title_Artificial Intelligence    -0.006593

Management    -0.037320

Communication    -0.075724

Job Title_Other    -0.113752

Location_East    -0.198398

Company_Small    -0.224192

Job Title_Software Developer    -0.225419

* Mean Squared Error (MSE): Calculated using mean_squared_error.

* R-squared (R²): Calculated using r2_score.

* Results:

    * XGBoost - Mean Squared Error: 12450.123046875

    * XGBoost - R-squared: 0.15793746709823608

            Skill Importance:
Description of Feature Importance Techniques:

* XGBoost Feature Importance: The feature_importances_ attribute of the XGBoost model was used to extract the importance of each feature (skill) for predicting job titles.
  
    * XGBoost Feature Importances for Job Title_Artificial Intelligence:
      
        * Management: 0.23763231933116913 
        * Programming: 0.38770297169685364
        * Communication: 0.3746647238731384

    * XGBoost Feature Importances for Job Title_Other:
        * Management: 0.23763231933116913
        * Programming: 0.38770297169685364
        * Communication: 0.3746647238731384

    * XGBoost Feature Importances for Job Title_Software Developer:
        * Management: 0.23763231933116913
        * Programming: 0.38770297169685364
        * Communication: 0.3746647238731384

    * XGBoost Feature Importances for Job Title_Software Engineer:
        * Management: 0.23763231933116913
        * Programming: 0.38770297169685364
        * Communication: 0.3746647238731384

* Random Forest Feature Importance: The feature_importances_ attribute of the RandomForestClassifier was used to extract the importance of each feature (skill) for predicting job titles.

    * Random Forest Feature Importances for Job Title_Artificial Intelligence:
        * Management: 0.22041738020028318 
        * Programming: 0.4447733828006535
        * Communication: 0.33480923699906334

    * Random Forest Feature Importances for Job Title_Other:
        * Management: 0.22041738020028318 
        * Programming: 0.4447733828006535
        * Communication: 0.33480923699906334

    * Random Forest Feature Importances for Job Title_Software Developer:
        * Management: 0.22041738020028318 
        * Programming: 0.4447733828006535
        * Communication: 0.33480923699906334

    * Random Forest Feature Importances for Job Title_Software Engineer:
        * Management: 0.22041738020028318 
        * Programming: 0.4447733828006535
        * Communication: 0.33480923699906334

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
  
![Figure_1111](https://github.com/user-attachments/assets/ec0b23fc-1244-4453-815b-146b1e1d2b11)

Bar plots were used to show the importance of different skills (e.g., Management, Programming, Communication) for each job role.

* Heatmaps:

![Figure_14](https://github.com/user-attachments/assets/00c00fb5-9961-4140-a4c9-2425d12bb282)

Heatmaps were created to visualize the importance of skills across different job roles.

#  Discussion and Conclusions
   
At first, the project did not seem so difficult to me until I started scraping. For several days, and maybe even weeks, I literally did not get the start of the project due to ignorance, various site structures, blocking, etc. I was glad when I finally dealt with this problem, even despite the long time the program ran. When it was time for preprocessing and model training, it was not easy either. It seems to me that I narrowed all the titles too much, which is why the result was not very correct.

But this project had many advantages, such as:

* Data scraping, the task itself was very interesting, inspecting html code, overcoming problems

* Working with information, classifying columns

* Studying and working with XGBoost

The project is very interesting and I am glad that I was able to achieve at least this result. I think that I could do more and better, understanding this topic more.
