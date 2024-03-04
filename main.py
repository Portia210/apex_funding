import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from plans_dict import plans_dict
from validations import *

# set the driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--headless')  # Enable headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
chrome_options.add_argument("accept-language=en-US;q=0.8,en;q=0.7")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get("https://www.apextraderfunding.com/member/member/")
print("----------------------------------------")
print("please wait for apex funding to load...")
time.sleep(2)

auth_success = False
while not auth_success:
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "amember-login")))
    password = driver.find_element(By.ID, "amember-pass")
    username.send_keys(input("enter username/email: "))
    password.send_keys(input("enter password: "))

    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(2)
    try:
        element_after_login = driver.find_element(By.ID, "widget-member-main-subscriptions")

        # Check if the element is present, indicating successful authentication
        if element_after_login.is_displayed():
            print("Authentication successful!")
            break
        else:
            print("Element isn't display")
    except NoSuchElementException:
        print("Authentication have failed.")

valid_type_choice = False
account_type = ""
while not valid_type_choice:
    rithmic_tradovate = input("type 1 for Rithmic, 2 for Tradovate: ")
    # rithmic_tradovate = "2"
    time.sleep(0.3)
    if rithmic_tradovate == "1":
        account_type = "Rithmic"
        valid_type_choice = True


    elif rithmic_tradovate == "2":
        valid_type_choice = True
        account_type = "Tradovate"

    else:
        print("uncorrected choice, select again:")

for i, plan in enumerate(plans_dict[account_type]):
    print(f"For {plan["plan_title"]}, press {i + 1}")

plan_index = int(input("Your Choice: ")) - 1
selected_plan = plans_dict[account_type][plan_index]
print("----------------------------------------------------------")
print(f"You Selected {selected_plan["plan_title"]}")
print("----------------------------------------------------------")
print("now you'll need to fill your billing details one time for the purchases, we do note save them, "
      "they will delete after the script will finish running")

# testing values
# first_name = "h"
# last_name = "h"
# credit_card_month = "12"
# credit_card_year = "2024"
# credit_card_number = "375510390001191"
# cvv_number = "222"

# collectiog values
cc_values = get_cc_details()

accounts_number = int(input("How many accounts would you like to purchase? "))
accounts_counter = 0
while accounts_counter < accounts_number:
    print(f"Purchasing account number {accounts_counter + 1}")
    driver.get(selected_plan["plan_link"])
    time.sleep(2)
    # fill details
    driver.find_element(By.CSS_SELECTOR, "input[name='coupon']").send_keys("SAVE90")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "fieldset input[type='checkbox']")
    for checkbox in checkboxes:
        time.sleep(0.1)
        driver.execute_script("arguments[0].checked = true;", checkbox)
        print(f"Agreed to {checkbox.get_attribute("placeholder")}")

    # move to payment
    next_btn = driver.find_element(By.CSS_SELECTOR, "input[value='Next']")
    driver.execute_script("arguments[0].scrollIntoView();", next_btn)
    time.sleep(1)
    next_btn.click()
    time.sleep(2)
    print("-----------------------------------")
    print("moving to filling your credit card details")


    # fill the cc derails
    cc_name_f = driver.find_element(By.ID, "cc_name_f")
    driver.execute_script("arguments[0].value = arguments[1]", cc_name_f, cc_values["first_name"])
    time.sleep(0.1)
    cc_name_l = driver.find_element(By.ID, "cc_name_l")
    driver.execute_script("arguments[0].value = arguments[1]", cc_name_l, cc_values["last_name"])
    time.sleep(0.1)
    cc_number = driver.find_element(By.ID, "cc_number")
    driver.execute_script("arguments[0].value = arguments[1]", cc_number, cc_values["credit_card_number"])
    time.sleep(0.1)
    select_month_elem = driver.find_element(By.NAME, "cc_expire[m]")
    select_month_obj = Select(select_month_elem)
    select_month_obj.select_by_value(cc_values["credit_card_month"])
    time.sleep(0.1)
    select_year_elem = driver.find_element(By.NAME, "cc_expire[y]")
    select_year_obj = Select(select_year_elem)
    select_year_obj.select_by_value(cc_values["credit_card_year"])
    time.sleep(0.1)
    driver.find_element(By.ID, "cc_code").send_keys(cc_values["cvv_number"])
    total_price = driver.find_element(By.CSS_SELECTOR, "tr.am-receipt-row-total .am-receipt-price strong")
    print("----------------------------------------------")
    print(f"finished to fill credit card details")
    print(f"total price for account number {accounts_counter + 1} is: {total_price.text}")
    confirmation = input("Type Y to confirm: ").strip().lower()

    if confirmation == "y":
        pay_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Subscribe And Pay']")
        driver.execute_script("arguments[0].scrollIntoView();", pay_btn)
        time.sleep(1)
        pay_btn.click()
        try:
            time.sleep(2)
            success_div = driver.find_element(By.CLASS_NAME, "am-thanks-status-success")
            print(success_div.text)
        except NoSuchElementException:
            print("Payment Failed")
            print("--------------------------------------")
            print("let's go through the details again...")
            cc_values = get_cc_details()
            accounts_counter -= 1
    else:
        print("You didn't confirm, existing...")
        break

time.sleep(3)
driver.close()
driver.quit()
