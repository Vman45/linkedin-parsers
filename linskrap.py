from selenium import webdriver
from parsel import Selector
import time


def skrap_emp(driver, username, password, company):
    """ logs in to linkedin.com using the given username & password, browses to 
    the target company, and extracts its employees and stores in a list """
    sleep_time = 1
    driver = webdriver.Chrome(driver)
    driver.get("https://www.linkedin.com/login")
    
    uid = driver.find_element_by_id("username")
    uid.send_keys(username)

    pwd = driver.find_element_by_id("password")
    pwd.send_keys(password)
    time.sleep(sleep_time)
    
    log_in_button = driver.find_element_by_class_name("login__form_action_container")
    log_in_button.click()
    time.sleep(sleep_time)

    driver.get("https://www.linkedin.com/company/" + company + "/people/")
    time.sleep(sleep_time)
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(sleep_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

    sel = Selector(text=driver.page_source)
    employees = sel.xpath("//div[@class='org-people-profile-card__profile-title t-black "
    "lt-line-clamp lt-line-clamp--single-line ember-view']/text()").getall()
    employees = [employee.strip() for employee in employees]
    return employees