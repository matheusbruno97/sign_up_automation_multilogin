import mlx_functions as mlx
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from env import *

driver, profile_id = mlx.instantiate_driver()

def automation():
    try:
        driver.get("https://temp-mail.org/en/")
        for _ in range(5): # check if the email address is still loading or not
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".emailbox-input.opentip.disabledText")))
                time.sleep(10)
            except Exception as e:
                break
        email_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".emailbox-input.opentip"))).get_attribute("value")
        driver.switch_to.new_window('tab')
        driver.get("https://trakt.tv/auth/join")
        time.sleep(5)
        for _ in range(5): # check if there are any cookie frames
            try:
                cookie_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.cm__btn")))
                for button in cookie_buttons[:1]:
                    button.click()
            except Exception as e:
                break

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user_email"))).send_keys(email_box)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user_username"))).send_keys(trakt_username)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user_password"))).send_keys(trakt_password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "user_password_confirmation"))).send_keys(trakt_password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accept_terms_privacy"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "commit"))).click()

        # Before switching tabs, I could assert I see the Welcome page
        # For the time being, I'll just add time.sleep
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(10)
        
        email_subjects = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.viewLink.title-subject")))
        for subject in email_subjects:
            driver.execute_script("arguments[0].scrollIntoView(true);", subject) # scroll down to click it
            if subject.accessible_name == "Confirm your email address":
                subject.click()
                break
        for _ in range(5): # check if the confirm button is there
            try:
                confirm_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/a')))
                break
            except Exception as e:
                time.sleep(10)

        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button) # scroll down to click it
        confirm_button.click()
        time.sleep(10)

    except Exception as e:
            print(f"Something happened: {e}")
            driver.quit()
    finally:
        driver.quit()
        mlx.stop_profile(profile_id)
    
automation()
