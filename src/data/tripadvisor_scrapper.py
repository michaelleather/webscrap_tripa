from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.support import EC
from selenium.webdriver.common.by import By

import time
import pandas as pd
import csv


#class
class Restaurant:
    'common base for all restaurants'
    def __init__(self, driver):
        self.driver = driver

    def get(self):
        #WebDriverWait(driver, 1).until(expected_conditions.find_element_by_xpath('//*[@id="component_45"]/div/div[1]/h1').text)
#        try:
#            self.name = WebDriverWait(driver, 1).until(expected_conditions.visibilityOfElementLocated(By.xpath('//*[@id="component_45"]/div/div[1]/h1'))).text
#        except:
#            preload = WebDriverWait(self.driver, 1).until(expected_conditions.presence_of_element_located((By.XPATH, '//video[contains(@preload,"auto")]')))
#            if preload == "auto":
#                driver.findElement(By.xpath('//video[contains(@preload,"auto")]')).setAttribute("preload", "false")    
        try:
            #self.name = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="component_45"]/div/div[1]/h1'))).text
            self.name = self.driver.find_element_by_xpath('//*[@id="component_45"]/div/div[1]/h1').text
            self.address = self.driver.find_element_by_xpath('//*[@id="component_45"]/div/div[3]/span[1]/span/a').text
            self.telephone = self.driver.find_element_by_xpath('//*[@id="component_45"]/div/div[3]/span[2]/span/span[2]/a').text
            self.website = self.driver.find_element_by_xpath('//*[@id="component_45"]/div/div[3]/span[3]/span/a').get_attribute('href')
            try:
                self.email = self.driver.find_element_by_xpath('//a[contains(@href,"mailto")]').get_attribute('href')
            except:
                self.email = "not_available"
        except:
            self.name = "not_available"
            self.address = "not_available"
            self.telephone = "not_available"
            self.website = "not_available"
            self.email = "not_available"

        return self.to_dict()
                     
    def to_dict(self):
        return {'name': self.name, 
                'address': self.address,
                'telephone': self.telephone,
                'website': self.website,
                'email': self.__emailClean__(self.email)
                }
    
    def __emailClean__(self, email):
        return email.replace("mailto:","").replace("?subject=?","")
    
class Restaurants:
    tripadvisor = 'https://www.tripadvisor.com/Restaurants-g187439-Marbella_Costa_del_Sol_Province_of_Malaga_Andalucia.html'
    
    def __init__(self, driver):
        self.driver = driver

    def pages(self):
        pages_xpath = "//a[string-length(@data-page-number)>0]"
        pages_numbers = self.driver.find_elements(By.XPATH, pages_xpath)
        page_list = []
        for page in pages_numbers:
            page_list.append(page.text)
        page_list = [int(s) for s in page_list if s.isdigit()]
        print(page_list)
        return max(page_list)
    
    def next_page(self, page_to_click):
        self.driver.find_element_by_xpath(f"//a[@data-page-number='{page_to_click}']").click()    
    
    def get(self):
        result = []
        self.driver.get(self.tripadvisor)
        WebDriverWait(self.driver, 1).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button.evidon-banner-acceptbutton'))).click()
        self.driver.window_handles
        print('todavia no hemos pasado pagina')
        max_page = self.pages()
        for j in range(1,43):
            min_range = (j-1)*30 if j > 1 else 1
            max_range = min_range + 30
            for i in range(min_range, max_range):
                try:
                    self.driver.find_element_by_xpath('//*[@id="component_2"]/div/div[%d]/span/div[1]/div[2]/div[1]/div/span/a' %(i)).click()
                    self.driver.switch_to.window(driver.window_handles[-1])
                    restaurant = Restaurant(self.driver).get()
                    print('pagina ' + str(j) + ' restaurante' + str(i))
                    print(restaurant)
                    result.append(restaurant)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    print("no_funciona")
            self.next_page(j+1)
            print('hemos pasado de pagina')
        WebDriverWait(driver, 1).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button.evidon-banner-acceptbutton'))).click()
        return result

if __name__ == "__main__":
    #Opciones de naveragion
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    #options.add_argument('--disable-extensions')
    driver_path = 'c:/Users/Michael/Desktop/Python Projects/TripAdvisor Web Scrapper/chromedriver.exe'
    driver = webdriver.Chrome(driver_path, chrome_options=options)
    myrestaurants = Restaurants(driver).get()
    print(myrestaurants)


df = pd.DataFrame.from_dict(myrestaurants)
df.to_csv('my_new_file.csv', index=False)
#import pandas as pd 
#
#
#data = [{'area': 'new-hills', 'rainfall': 100, 'temperature': 20}, 
#		{'area': 'cape-town', 'rainfall': 70, 'temperature': 25}, 
#		{'area': 'mumbai', 'rainfall': 200, 'temperature': 39 }] 
#
#df = pd.DataFrame.from_dict(data) 
#
#df 
#despues hacer el import csv

#        time.sleep(2)
#works
#driver.find_element_by_xpath('//*[@id="component_2"]/div/div[2]/span/div[1]/div[2]/div[1]/div').click()
    
#works
#driver.switch_to.window(driver.window_handles[-1])
        

#third
#//*[@id="component_2"]/div/div[3]/span/div[1]/div[2]/div[1]/div/span/a
#fourth
#//*[@id"component_2"]/div/div[4]/span/div[1]/div[2]/div[1]/div/span/a

#get data from restaurant

        
#        try:
#            rest1 = Restaurant(name.text, address.text, telephone.text, website.get_attribute('href'), email.get_attribute('href'))
#        except:
#            rest1 = Restaurant(name.text, address.text, telephone.text, website.get_attribute('href'), email = "not_available")




# Prepare CSV file
#csvFile = open("restaurants.csv", "w", newline='', encoding="utf-8")
#csvWriter = csv.writer(csvFile)
#csvWriter.writerow(['name','address','telephone','website','email'])
#
##if restaurant doesnt have email then assign text
#try:
#    csvWriter.writerow((name.text, address.text, telephone.text, website.get_attribute('href'), email.text))
#except:
#    csvWriter.writerow((name.text, address.text, telephone.text, website.get_attribute('href'), email.get_attribute('href')))
#
## Close CSV file and browser
#csvFile.close()
#        driver.close()
 #