from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import json
import getpass
from datetime import datetime
import os
import pandas as pd
import openpyxl

class FacebookGroupScrapper:
    def __init__(self):
        print('\n=====FACEBOOK GROUP MEMBER SCRAPPER========')

    def get_config(self):
        try:
            # thong tin dang nhap
            print('Nhap thong tin dang nhap: ')
            self.email = input('Email/UserName: ').strip()
            self.password = getpass.getpass('Password: ')

            # iD group
            print('\nNhap ID group facebook: ')
            self.group_id = input('Group ID: ').strip()

            # so lan scroll
            print('\nSo lan scroll de load  them thanh vien: ')
            self.scroll_count = int(input('So lan scroll (mac dinh 5)') or "5")


        except Exception as e:
            print(e)
            pass

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            print(e)
            pass

    def login(self):
        try: 
            self.driver.get('https://www.facebook.com/')

            # Nhap email
            email_input = self.driver.find_element(By.ID, 'email')
            email_input.send_keys(self.email)

            # Nhap pass
            pass_input = self.driver.find_element(By.ID, 'pass')
            pass_input.send_keys(self.password)

            # Click dang nhap
            login_button = self.driver.find_element(By.NAME, 'login')
            login_button.click()

            time.sleep(10)
            print('Dang nhap thanh cong')
            return True
        except Exception as e:
            print(e)
            return False
        
    def save_members_to_excel(self, members, file_name="group_members.xlsx"):
        try:
            members_list = [{"User ID": user_id, "Name": name} for user_id, name in members]
            df = pd.DataFrame(members_list)
            df.to_excel(file_name, index=False)
            print(f"Data saved to {file_name}")
        except Exception as e:
            print(f"Error saving members to Excel: {e}")

    def get_group_members(self):
        
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(10)

            user_id_set = set()
            members = set() # dung set de khong bi trung lap


            for i in range(self.scroll_count):
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(10)
                print(f'scroll lan {i+1}/{self.scroll_count}')

                # Thu thap thong tin sau moi lan scroll
                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                for user in user_elements:
                    try:
                        href = user.get_attribute('href')
                        if '/user/' in href:
                            user_id = href.split('/')[6]
                            # Try extracting name from text or nested elements
                            name = user.text.strip()
                            if not name:  # If name is empty, try other strategies
                                try:
                                    name = user.find_element(By.TAG_NAME, 'span').text.strip()
                                except:
                                    name = user.get_attribute('aria-label')  # Check alternative attributes

                            if user_id not in user_id_set and name:  # Avoid duplicates and empty names
                                user_id_set.add(user_id)
                                members.add((user_id, name))
                                print(user_id, '-', name)
                    except Exception as e:
                        print(e)
                        pass
            # Save members to an Excel file
            self.save_members_to_excel(members)

        except Exception as e:
            print(e)
            pass

def main():
    scrapper = None
    try:
        scrapper = FacebookGroupScrapper()
        scrapper.get_config()
        scrapper.setup_driver()
        if scrapper.login():
            scrapper.get_group_members()
            print('--------------')
            time.sleep(10)
        time.sleep(10)
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()