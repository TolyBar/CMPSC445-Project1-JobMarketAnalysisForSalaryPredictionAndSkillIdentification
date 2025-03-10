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
   
![Figure_1](https://github.com/user-attachments/assets/b693e0df-575b-4210-a480-1a267fd62d93)

![Figure_2](https://github.com/user-attachments/assets/a3710bce-fa28-41ea-a29a-f99c98046219)

![Figure_3](https://github.com/user-attachments/assets/a728debb-d665-4f48-a9fc-7b1e171c038a)

![Figure_4](https://github.com/user-attachments/assets/2ab8fbb7-61fa-4321-8df2-6c7c6afb03cc)

![Figure_5](https://github.com/user-attachments/assets/4d9b8948-948c-46ed-980f-a65e0e928ca9)

![Figure_6](https://github.com/user-attachments/assets/c0a1f969-8ac6-417d-b46b-abb84c674fe7)

![Figure_7](https://github.com/user-attachments/assets/33fcce14-ef2b-460a-ad7e-f0d407b8f581)

![Figure_14](https://github.com/user-attachments/assets/00c00fb5-9961-4140-a4c9-2425d12bb282)

![Figure_13](https://github.com/user-attachments/assets/f4af0dd4-541d-46d3-b550-a62f5a12922d)

![Figure_12](https://github.com/user-attachments/assets/182e981f-69b8-48e2-a27d-1a2ecf9204a7)

![Figure_11](https://github.com/user-attachments/assets/43e456ab-091f-4957-ad0b-1adefec402e1)

![Figure_10](https://github.com/user-attachments/assets/c9b2fa97-17a0-42bb-9812-eba39a72c966)

![Figure_9](https://github.com/user-attachments/assets/a394c7ea-f147-479b-aafc-a3e76540e15b)

![Figure_8](https://github.com/user-attachments/assets/dfe132fb-a621-454b-a458-eb475b9671e5)

#  Discussion and Conclusions
   
Project Findings: The analysis provided insights into the most demanded skills for various job roles in the tech industry. Python, SQL, and JavaScript emerged as top skills across multiple roles.
Challenges Encountered: Handling inconsistencies in job titles and qualifications, integrating data from different sources, and extracting relevant skills from job descriptions. Scraping posed a great challenge in the beginning as I had to not only iterate through a huge amount of listings, but also idenitfy and interact with things like buttons to display more jobs, which were different across each site and listings that were incomplete or varied from each other.
Recommendations: To improve model performance, I could utilize more advanced techniques to better extract and standardize skills from job descriptions, identify more features, and continuously update the dataset to reflect current market trends.
