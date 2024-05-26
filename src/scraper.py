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
        self.driver = webdriver.Chrome() # Certifique-se de que o ChromeDriver está instalado e no PATH
        self.url = url
        self.navigation_path = navigation_path
        self.download_dir = download_dir 
        self.filenames = files

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def scroll_half_of_display(self):
        self.driver.execute_script("window.scrollTo(0, window.innerHeight / 2);")
        time.sleep(1)  # Tempo para garantir que o conteúdo carregue

    def navigate_to_target_page(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 10)

        for navigation_text in self.navigation_path:
            print(f"Clique em '{navigation_text}'")
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, navigation_text))).click()
            self.scroll_half_of_display()

    def download_files(self):
        # Nomes dos arquivos a serem baixados
        filenames = self.filenames

        self.scroll_half_of_display()

        for filename in filenames:
            print(f"Procurando e clicando no link para o arquivo: {filename}")
            link = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{filename}')]"))
            )
            link.click()
            time.sleep(1)  # Espera para o download ser concluídoS
            self.move_file(filename)

    def move_file(self, filename):
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
        destination_path = os.path.join(self.download_dir, filename)
        if os.path.exists(default_download_path):
            print(f"Movendo arquivo {filename} para {self.download_dir}")
            shutil.move(default_download_path, destination_path)
        else:
            print(f"Arquivo {filename} não encontrado no diretório de downloads")


    def close(self):
        print("Fechando navegador")
        self.driver.quit()
