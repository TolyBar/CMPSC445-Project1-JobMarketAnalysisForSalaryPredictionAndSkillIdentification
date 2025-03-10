from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument("--disable-dev-shm-usage")

# Selenium with ChromeDriver
service = Service("C:\\Users\\admin\\OneDrive\\Рабочий стол\\Coding\\JobScrape\\chromedriver-win64\\chromedriver.exe") # Edit to you path

# Function to start the Chrome WebDriver
def start_driver():
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to load more jobs
def load_more_jobs(driver, target_jobs=2000):
    current_jobs = 0
    while current_jobs < target_jobs:
        try:
            # Wait for the "Load More" button to be clickable
            load_more_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-test='load-more']"))
            )
            # Click the "Load More" button
            load_more_btn.click()
            # Wait for new jobs to load
            time.sleep(3)  # Adjust sleep time if needed

            # Update the number of visible jobs
            job_elements = driver.find_elements(By.CLASS_NAME, "JobCard_jobCardContainer__arQlW")
            current_jobs = len(job_elements)
            print(f"Loaded {current_jobs} jobs so far...")

            # Stop if we've reached the target
            if current_jobs >= target_jobs:
                break
        except Exception as e:
            print("No more 'Load More' button or error:", e)
            break  # Stop the loop if the button is not found or an error occurs

# Function to parse the location text and extract the state or "Remote"
def parse_location(location_text):
    
    # Check if the location is remote
    if "remote" in location_text.lower():
        return "Remote"
    else:
        # Split the location text by comma and get the last part (state)
        parts = location_text.strip().split(",")
        if len(parts) > 1:
            state = parts[-1].strip()  # Get the state abbreviation (e.g., "IL")
        else:
            state = location_text.strip()  # Get the full location if no comma is found (e.g., "Colorado")

        # Convert full state names to abbreviations if necessary
        state_abbreviations = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
            "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
            "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
            "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
            "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
            "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
            "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
            "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
            "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
            "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
            "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
        }

        # Convert full state name to abbreviation if applicable
        return state_abbreviations.get(state, state)  # Return abbreviation if found, otherwise return the original state

# Scrape job element from GlassDoor
def scrape_job_element_GlassDoor(job_element):
    try:
        # Job Title
        job_title = job_element.find_element(By.XPATH, ".//a[@data-test='job-title']").text
    except:
        job_title = "Not Available"

    try:
        # Company Name
        company = job_element.find_element(By.XPATH, ".//span[contains(@class, 'EmployerProfile_compactEmployerName__')]").text
    except:
        company = "Not Available"

    try:
        # Location
        location_element = job_element.find_element(By.XPATH, ".//div[@data-test='emp-location']")
        location_text = location_element.text
        location = parse_location(location_text)  # Extract state or "Remote"
    except:
        location = "Not Available"

    try:
        # Salary
        salary = job_element.find_element(By.XPATH, ".//div[@data-test='detailSalary']").text
    except:
        salary = "Not Provided"

    try:
        # Extract the Skills from the <b>Skills:</b> tag
        skills_element = job_element.find_element(By.XPATH, ".//div[@data-test='descSnippet']//div[contains(b, 'Skills:')]")
        skills = skills_element.text.replace("Skills:", "").strip()
    except:
        skills = "Not Provided"

    try:
        # Job Description Snippet
        description = job_element.find_element(By.XPATH, ".//div[@data-test='descSnippet']").text
    except:
        description = "Not Available"

    # Return the job data
    return {
        "Job Title": job_title,
        "Company": company,
        "Location": location,  # Now contains only the state abbreviation or "Remote"
        "Salary": salary,
        "Skills": skills,
        "Description": description
    }

# Scrape job element from SimplyHire
def scrape_job_element_SimplyHire(job_element):
    salary_selectors = [
    'p.chakra-text.css-1ejkpji',
    'p.chakra-text.css-1g1y608',
    'p.chakra-text.css-1g1y608' 
]
    # Extract the job title, company, location, and salary
    try:
        job_title = job_element.find_element(By.CSS_SELECTOR, 'h2.chakra-text.css-8rdtm5').text
    except:
        job_title = "Not Available"
    try:
        company = job_element.find_element(By.CSS_SELECTOR, 'span.css-lvyu5j').text.rstrip(" —")
    except:
        company = "Not Available"
    try:
        location_element = job_element.find_element(By.CSS_SELECTOR, 'span.css-1t92pv')
        location_text = location_element.text
        location = parse_location(location_text)  # Extract state or "Remote"
    except:
            location = "Not Available"
    
    # Extract the salary from one of the possible selectors
    salary = None
    for selector in salary_selectors:
        try:
            salary = job_element.find_element(By.CSS_SELECTOR, selector).text
            if salary:  # If salary is found, break out of the loop
                break
        except:
            continue

    #Return the job data
    return {
        "Job Title": job_title,
        "Company": company,
        "Location": location,  # Now contains only the state abbreviation or "Remote"
        "Salary": salary,
        "Skills": "Not Provided"
    }
    
# Scrape jobs from GlassDoor
def scrape_jobs_GlassDoor(driver):
    jobs_data = []
    job_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "JobCard_jobCardContainer__arQlW"))
    )

    for job_element in job_elements:
        job_data = scrape_job_element_GlassDoor(job_element)
        jobs_data.append(job_data)

    return jobs_data

# Scrape jobs from SimplyHire
def scrape_jobs_SimlyHire(driver):
    jobs_data = []
    job_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.css-0'))
    )

    for job_element in job_elements:
        job_data = scrape_job_element_SimplyHire(job_element)
        jobs_data.append(job_data)

    return jobs_data

# Save data to CSV
def save_to_csv(data, filename="jobs.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, mode='a', header=not pd.io.common.file_exists(filename))


# Main Execution
def main():

    # URLs to scrape
    urls_1 = [
        "https://www.glassdoor.com/Job/new-york-state-software-engineer-jobs-SRCH_IL.0,14_IS428_KO15,32.htm",
        "https://www.glassdoor.com/Job/california-us-software-engineer-jobs-SRCH_IL.0,13_IS2280_KO14,31.htm",
        "https://www.glassdoor.com/Job/florida-us-software-engineer-jobs-SRCH_IL.0,10_IS3318_KO11,28.htm",
        "https://www.glassdoor.com/Job/massachusetts-us-software-engineer-jobs-SRCH_IL.0,16_IS3399_KO17,34.htm",
        "https://www.glassdoor.com/Job/maryland-us-software-engineer-jobs-SRCH_IL.0,11_IS3201_KO12,29.htm",
        "https://www.glassdoor.com/Job/oregon-us-software-engineer-jobs-SRCH_IL.0,9_IS3163_KO10,27.htm",
        "https://www.glassdoor.com/Job/washington-state-us-software-engineer-jobs-SRCH_IL.0,19_IS3020_KO20,37.htm"
    ]

    # Scrape jobs from each URL
    for url in urls_1:
        # Start the WebDriver
        driver = start_driver()
        # Load the URL
        driver.get(url)

        # Scrape jobs from GlassDoor
        try:
            # Load more jobs until we reach 800 or no more "Load More" buttons
            load_more_jobs(driver, target_jobs=800)

            # Scrape all jobs
            jobs_data = scrape_jobs_GlassDoor(driver)
            # Save the data to a CSV file
            save_to_csv(jobs_data)
        finally:
            # Close the WebDriver
            driver.quit()

    # URLs to scrape
    urls_2 = [
        "https://www.simplyhired.com/search?q=software+engineer&l=New+York+State",
        "https://www.simplyhired.com/search?q=software+engineer&l=California",
        "https://www.simplyhired.com/search?q=software+engineer&l=Florida",
        "https://www.simplyhired.com/search?q=software+engineer&l=Massachusetts",
        "https://www.simplyhired.com/search?q=software+engineer&l=Maryland",
        "https://www.simplyhired.com/search?q=software+engineer&l=Oregon",
        "https://www.simplyhired.com/search?q=software+engineer&l=Washington+State"
    ]

    # Scrape jobs from each URL
    for url in urls_2:
        # Start the WebDriver
        driver = start_driver()
        # Load the URL
        driver.get(url)

        # Scrape jobs from SimplyHire
        try:
        # Load more jobs until we reach 800 or no more "Load More" buttons
            load_more_jobs(driver, target_jobs=800)

        # Scrape all jobs
            jobs_data = scrape_jobs_SimlyHire(driver)
            # Save the data to a CSV file
            save_to_csv(jobs_data)
        finally:
            # Close the WebDriver
            driver.quit()
    # Print a message to indicate that the scraping is complete
    print("Scraping completed.")

# Run the main function
if __name__ == "__main__":
    main()

