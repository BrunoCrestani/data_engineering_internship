import os
import time
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper:

    def __init__(self, url, navigation_path, download_dir, files):
        self.driver = webdriver.Chrome()         
        self.url = url
        self.navigation_path = navigation_path
        self.download_dir = download_dir 
        self.filenames = files

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    # method to scroll the display 
    def scroll_half_of_display(self):
        self.driver.execute_script("window.scrollTo(0, window.innerHeight / 2);")
        time.sleep(1)  

    # method to interact with the webpage
    def navigate_to_target_page(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)
        # Clicks on the buttons accordingly to the recieved navigation_path
        for navigation_text in self.navigation_path:
            print(f"Click on '{navigation_text}'")
            # Waits and clicks in the button that corresponds to the navigatio_text
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, navigation_text))).click()
            self.scroll_half_of_display()

    # method to download the requested files
    def download_files(self):
        filenames = self.filenames

        self.scroll_half_of_display()

        # Clicks on the download links accordingly to the received filenames
        for filename in filenames:
            print(f"Searching and clicking the link for the archive: {filename}")
            # finds the link
            link = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{filename}')]")))

            #clicks on it
            link.click()
            time.sleep(1)              
            self.move_file(filename)

    # method to move the downloaded files to a directory in the project
    def move_file(self, filename):
        # gets the deafult path
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        # gets the destination path
        destination_path = os.path.join(self.download_dir, filename)
        # verifies if the file is in the default path 
        if os.path.exists(default_download_path):
            print(f"Moving file {filename} to {self.download_dir}")
            # moves the file to destination
            shutil.move(default_download_path, destination_path)
        else:
            print(f"File {filename} not found in the Downloads directory")

    # Method to close the browser
    def close(self):
        print("Closing Nav")
        self.driver.quit()
