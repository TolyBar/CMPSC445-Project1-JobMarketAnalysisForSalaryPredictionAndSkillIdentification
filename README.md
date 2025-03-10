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

Web scraping job listings from SimplyHired and Glassdoor. Each group of listing comes from a simple search for Software Engineering roles on the respective site.

Extracting job titles, companies, locations, description, and skills.

Tools Used: Selenium, pandas, scikit-learn, matplotlib.

Data Sources: SimplyHired, Glassdoor.

Collected Attributes: Job title, company, location, skills, description.

Number of Data Samples: 4000+ job listings.

2. Data Preprocessing:



3. Feature Engineering:


4. Model Development and Evaluation:
   
Train and Test Data Partition: Splitting data into training (80%) and testing (20%) sets.

  Salary Prediction : Model-1

  Salary Prediction : Model-2

  Skill Importance:

5. Visualization
   

#  Discussion and Conclusions
   
Project Findings: The analysis provided insights into the most demanded skills for various job roles in the tech industry. Python, SQL, and JavaScript emerged as top skills across multiple roles.
Challenges Encountered: Handling inconsistencies in job titles and qualifications, integrating data from different sources, and extracting relevant skills from job descriptions. Scraping posed a great challenge in the beginning as I had to not only iterate through a huge amount of listings, but also idenitfy and interact with things like buttons to display more jobs, which were different across each site and listings that were incomplete or varied from each other.
Recommendations: To improve model performance, I could utilize more advanced techniques to better extract and standardize skills from job descriptions, identify more features, and continuously update the dataset to reflect current market trends.
