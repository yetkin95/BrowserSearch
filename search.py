from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re

# WebDriver'ı başlat
driver = webdriver.Chrome()

# Kullanıcıdan arama terimini al
search_query = input("Arama yapmak istediğiniz kelimeleri girin: ")

# Google'da arama yap
driver.get(f"https://www.google.com/search?q={search_query}")

time.sleep(3)

all_page_links = []

for page_num in range(0, 10):  # 10 sayfa (0-9 arasındaki sayfalar)
    if page_num > 0:
        next_page_button = driver.find_element(By.XPATH, f'//a[@aria-label="Page {page_num + 1}"]')
        next_page_button.click()
        time.sleep(2)  

    links = driver.find_elements(By.XPATH, '//a[contains(@href, "http") and not(contains(@href, "google.com"))]')
    for link in links:
        href = link.get_attribute('href')
        if href and href.startswith('http'):
            all_page_links.append(href)

# Sonuçları dosyaya keydet
with open('google_search_results.txt', 'w', encoding='utf-8') as file:
    for page_url in all_page_links:
        try:
            driver.get(page_url)
            time.sleep(2)  
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()
            
            if text: 
                file.write(f"URL: {page_url}\n")
                file.write(f"Content: {text}\n\n" + "="*80 + "\n\n")
        except Exception as e:
            print(f"Hata oluştu: {e}")

driver.quit()

print("Sonuçlar kaydedildi: google_search_results.txt")
