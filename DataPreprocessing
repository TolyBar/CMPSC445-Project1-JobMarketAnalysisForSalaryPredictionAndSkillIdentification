import pandas as pd

# 1. Loading the Data and Filling Missing Values
df = pd.read_csv('jobs.csv')

df.fillna({"Salary": "N/A", "Skills": "N/A"}, inplace=True)


# 2: Standardizing Job Titles and Skills
df['Job Title'] = df['Job Title'].str.replace(r' - .*', '', regex=True)  # Remove extra descriptions
df['Job Title'] = df['Job Title'].str.strip()  # Remove leading/trailing spaces
df['Job Title'] = df['Job Title'].str.replace(r'["\']', '', regex=True)  # Remove single and double quotes

def standardize_title(title):
    title = title.strip()
    if any(keyword in title for keyword in ["AI", "Machine Learning", "Automation", "Robotics", "Artificial Intelligence"]):
        return "Artificial Intelligence"
    elif "Software" in title or "Engineer" in title:
        return "Software Engineer"
    elif "Developer" in title or "Programmer" in title:
        return "Software Developer"
    return "Other"
df['Job Title'] = df['Job Title'].apply(standardize_title)

# Standardizing Skills
df['Skills'] = df['Skills'].str.replace("Dev-Ops", "DevOps")  # Standardize DevOps variations
df['Skills'] = df['Skills'].str.replace("C Plus Plus", "C++")  # Standardize C++ variations

# Standardizing Locations
df['Location'] = df['Location'].str.replace("United States", "US")
df['Location'] = df['Location'].str.replace("Manhattan", "NY").str.replace("New York", "NY").str.replace("NY State", "NY").str.replace("NYville", "NY")
df['Location'] = df['Location'].str.replace("Patuxent River Naval Air Station", "MD")
df['Location'] = df['Location'].str.replace("Joint Base Lewis McChord", "WA").str.replace("Washington State", "WA")

df['Location'] = df['Location'].apply(lambda x: "East" if "NY" in x else x)
df['Location'] = df['Location'].apply(lambda x: "West" if "WA" in x else x)
df['Location'] = df['Location'].apply(lambda x: "West" if "OR" in x else x)
df['Location'] = df['Location'].apply(lambda x: "West" if "CA" in x else x)
df['Location'] = df['Location'].apply(lambda x: "East" if "FL" in x else x)
df['Location'] = df['Location'].apply(lambda x: "East" if "MA" in x else x)
df['Location'] = df['Location'].apply(lambda x: "East" if "MD" in x else x)
df['Location'] = df['Location'].apply(lambda x: "US" if "US" in x else x)

# Standardizing Company Size
def categorize_company(company):
    large_companies = ["Google", "Microsoft", "Amazon", "Apple", "Meta", "Tesla", "Netflix", "IBM", "Adobe", "Facebook"]
    return "Large" if any(comp in company for comp in large_companies) else "Small"
df['Company'] = df['Company'].apply(categorize_company)

# Step 3: Handling Salary Data
def calculate_mean_salary(salary):
    if salary == "Not Provided":
        return None  # Returning None for "Not Provided" (to be handled later)
    # Removing "(Glassdoor est.)" if present
    salary = salary.split(" (Glassdoor est.)")[0]
    # Removing "(Employer est.)" if present
    salary = salary.split(" (Employer est.)")[0]
    salary = salary.replace("From ", "").replace("Estimated: ", "").replace("Up to ", "")
    # Replace "a year" with an empty string and "an hour" with "Per Hour"
    salary = salary.replace(" a year", "").replace(" an hour", " Per Hour")
    
    # Handling hourly wages
    if "Per Hour" in salary:
        # Extract the numeric part (e.g., "$30.00 - $50.00 Per Hour" or "$40.00 Per Hour")
        salary = salary.replace(" Per Hour", "")
        if "-" in salary:
            # Handling hourly wage ranges (e.g., "$30.00 - $50.00")
            lower, upper = salary.split(" - ")
            lower = float(lower.replace("$", ""))
            upper = float(upper.replace("$", ""))
            mean_hourly = (lower + upper) / 2
        else:
            # Handling single hourly wage (e.g., "$40.00")
            mean_hourly = float(salary.replace("$", ""))
        # Converting to yearly salary (40 hours/week * 52 weeks/year)
        yearly_salary = mean_hourly * 40 * 52
        return int(yearly_salary)  # Return as integer
    # Handling missing salary values
    elif not salary or salary.strip().upper() in ['N/A', 'NA', '']:
        return None  # Indicate that this entry should be dropped
    # Handling yearly salary ranges (e.g., "$87K - $91K")
    elif "-" in salary:
        # Spliting the range into lower and upper bounds
        lower, upper = salary.split("-")  # Split on hyphen (no spaces assumed)
        
        # Cleaning and converting lower bound
        lower = lower.replace("$", "").replace("K", "").replace("M", "").replace(",", "").strip()
        lower = float(lower)
        if "K" in salary:  # Handle thousands
            lower *= 1000
        elif "M" in salary:  # Handle millions
            lower *= 1000000
        
        # Cleanig and converting upper bound
        upper = upper.replace("$", "").replace("K", "").replace("M", "").replace(",", "").strip()
        upper = float(upper)
        if "K" in salary:  # Handle thousands
            upper *= 1000
        elif "M" in salary:  # Handle millions
            upper *= 1000000
        
        # Calculating mean salary
        mean_salary = (lower + upper) / 2
        return int(mean_salary)  # Return as integer
    else:
        # Handling single salary (not a range)
        salary = salary.replace("$", "").replace(",", "").strip()
        if "K" in salary:
            salary = float(salary.replace("K", "")) * 1000
        elif "M" in salary:
            salary = float(salary.replace("M", "")) * 1000000
        else:
            salary = float(salary)
        return int(salary)  # Return as integer
    
# Applying the function to the Salary column to create a new column with integer salaries
df["Salary"] = df["Salary"].apply(calculate_mean_salary)

# Removing rows with missing salary values (after applying the extraction function)
df = df[df['Salary'].notna()]  # Remove rows with non-numeric salaries

# Step 4: Extracting Salary Information by splitting the skills column into a list of individual skills
def categorize_skills(skills):
    communication_skills = ['Communication skills', 'English', 'Writing skills']
    programming_skills = ['Jira', 'SQL', 'C#', 'C++', 'CI/CD', 'Bamboo', 'Web development', 'DevOps', 'Cabling']
    management_skills = ['Management', 'Microsoft Office', 'Inventory control', 'Budgeting']
    
    skills_list = skills.split(',') if isinstance(skills, str) else []
    
    return pd.Series({
        'Communication': int(any(skill.strip() in communication_skills for skill in skills_list)),
        'Programming': int(any(skill.strip() in programming_skills for skill in skills_list)),
        'Management': int(any(skill.strip() in management_skills for skill in skills_list))
    })

df[['Communication', 'Programming', 'Management']] = df['Skills'].apply(categorize_skills)
df.drop(columns=['Skills'], inplace=True)

# Saving the cleaned data to a CSV file
df.to_csv("preprocessed_jobs.csv", index=False)

print("Data preprocessing is complete and saved to 'preprocessed_jobs.csv'.")

