from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt
start_time = time.time()
def loading_data():
    html_content = driver.page_source
    

    soup = BeautifulSoup(html_content, "html.parser")
    for MAIN_URL in MAIN_URLS:
        try:
       
            
           
            ranking_elements = soup.find_all("div", class_="rankingType rankingType--odd")
            ranking_elements1 = soup.find_all("div", class_="rankingType rankingType--even")
            ranking_elements.extend(ranking_elements1)
            
            for element in ranking_elements:
                title = element.text.strip()  
                film_data.append( title)
                # time.sleep(random.randint(0,1))
                print("loading.........")
               

        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania {MAIN_URL}: {e}")
    return film_data


MAIN_URLS = [
    "https://www.filmweb.pl/ranking/film"

]


film_data = []

options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options = options   )

driver.get("https://www.filmweb.pl/ranking/film")
driver.maximize_window()

body = driver.find_element(By.TAG_NAME, 'body')  

time.sleep(5)





film_data = []

try:
    cookies_button = driver.find_element(By.ID, "didomi-notice-agree-button")
    cookies_button.click()
    time.sleep(2)
except Exception:
    pass

time.sleep(0)
body.send_keys(Keys.ESCAPE)

for i in range(170):
    time.sleep(random.randint(0,1))  
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    # if i == 80:
    #     loading_data()
        
    
       
    #     time.sleep(2)
    # else: 
    #     continue





loading_data()
film_data = [re.sub(r'https://\S+', '', item).strip() for item in film_data]
print(film_data)


pattern = r"""
    (?P<title>.+?)               
    (?P<year>\d{4})             
    \s                          
    (?P<rating>\d{1,2},\d{2})    
    \s10\s                       
    (?P<votes>[\d\s]+)           
"""


film_df = pd.DataFrame(film_data, columns=["raw_data"])

film_df = film_df["raw_data"].str.extract(pattern, flags=re.VERBOSE)


film_df["votes"] = film_df["votes"].str.replace(" ", "", regex=False).astype(int)


film_df["rating"] = film_df["rating"].str.replace(",", ".").astype(float)

film_df["year"] = film_df["year"].astype(int)
driver.quit()




output_path = r"C:\Users\Admin\Desktop\filmweb.csv"
film_df.to_csv(output_path, index=False)
print(f"Dane zapisano w pliku: {output_path}")
film_df.to_excel(r"C:\Users\Admin\Desktop\filmweb.xlsx")
end_time = time.time()
execution_time = end_time - start_time
print(f"code execution time: ", execution_time)