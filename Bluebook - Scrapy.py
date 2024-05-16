from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

keyword = "aggregates"
location = "NY, New York"
driver = webdriver.Chrome()
driver.get("https://www.thebluebook.com/search.html?searchTerm=" + keyword + "&regionLabel=" + location)

def print_company_details(company):
    company_name_element = company.find_element(By.CSS_SELECTOR, "div.cname-wrapper h3.cname")
    company_name = company_name_element.text
    print("Company Name:", company_name)
    
    # Extract serving areas
    serving_areas = company.find_element(By.CLASS_NAME, "serving-areas").text
    print("Serving Areas:", serving_areas)
    
    # Extract keywords
    keywords = [keyword.text for keyword in company.find_elements(By.CSS_SELECTOR, "ul.classification-list li")]
    print("Keywords:", keywords)
    
    # Extract iProView value
    try:
        iproview_element = company.find_element(By.CSS_SELECTOR, "div.header a.company-name-btn")
        iproview_value = iproview_element.get_attribute("href")
        print("iProView Value:", iproview_value)
        
        # Open iProView URL in a new tab
        driver.execute_script("window.open('" + iproview_value + "', 'new_window')")
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Extract website URL
        try:
            website_element = driver.find_element(By.CSS_SELECTOR, "a.pvInfo-website")
            website_url = website_element.get_attribute("href")
            print("Website:", website_url)
        except NoSuchElementException:
            print("Website URL not found")
        
        # Extract phone number
        try:
            phone_element = driver.find_element(By.CSS_SELECTOR, "a.telLink")
            phone_number = phone_element.get_attribute("data-dialnumber")
            print("Phone Number:", phone_number)
        except NoSuchElementException:
            print("Phone Number not found")
        
        # Close the tab after extracting information
        driver.close()
        # Switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])
        
    except NoSuchElementException:
        print("iProView Value not found")
    
    print("-" * 50)

def click_next_button():
    try:
        next_button = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Next')]")))
        next_button.click()
        return True
    except:
        return False

counter = 0
while True:
    companies = WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "media")))

    counter += len(companies)

    for company in companies:
        print_company_details(company)

    if not click_next_button():
        break

    time.sleep(4)

print("Counter: ", counter)

# Close the browser
driver.quit()
