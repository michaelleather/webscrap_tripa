from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import time
import pandas as pd
import csv


#class
class Restaurant:
    'common base for all restaurants'
    def __init__(self, driver):
        self.driver = driver

    def __get_element_text(self, xpath, attribute):
        try:
            element = self.driver.find_element_by_xpath(xpath)
            if attribute == "text":
                return element.text
            else:
                return element.get_attribute('href')
        except Exception as e:
            # print("Error while loading restaurant " + str(e))
            return "not_available"

    def get(self):
        self.name = self.__get_element_text("//h1[@data-test-target='top-info-header']", "text")
        self.address = self.__get_element_text("//a[@href='#MAPVIEW']", "text")
        self.telephone = self.__get_element_text("//a[contains(@href,'tel:')]", "text")
        self.website = self.__get_element_text("//a[contains(text(),'Website')]", "get")
        self.email = self.__get_element_text('//a[contains(@href,"mailto")]', "get")

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
    tripadvisor = "https://www.tripadvisor.com/Restaurants-g187439-Marbella_Costa_del_Sol_Province_of_Malaga_Andalucia.html"
    xpath_next = "//a[contains(text(),'Next')]"
    
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

    def next_button(self):
        return self.driver.find_element_by_xpath(self.xpath_next)

    def is_next_present(self):
        a = self.next_button()
        return a is not None

    def goto_next(self, page_range):        
        try:            
            driver.execute_script(f"arguments[0].setAttribute('data-offset', '{page_range}')", self.next_button())
            self.next_button().click()
        except:
            driver.execute_script(f"arguments[0].setAttribute('data-offset', '{page_range}')", self.next_button())
            print("despues de script")
            driver.execute_script("arguments[0].click();", self.next_button())

    def open_new_browser(self):
        self.driver.get(self.tripadvisor)        
        self.driver.window_handles

    def open_restaurants(self, j):        
        result = []
        links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/Restaurant_Review') and @target='_blank' and text()]")

        for i, link in enumerate(links):
            try:
                link_to_restaurant = link
                driver.execute_script("arguments[0].click();", link_to_restaurant)
                self.driver.switch_to.window(driver.window_handles[-1])
                restaurant = Restaurant(self.driver).get()
                print(f"Page {str(j)} restaurante {str(i)} {restaurant.get('name')} with email {restaurant.get('email')}")
                result.append(restaurant)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print("Error message " + str(e))

    def get(self):
        result = []
        self.open_new_browser()
        # WebDriverWait(self.driver, 1).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button.evidon-banner-acceptbutton'))).click()
        print('todavia no hemos pasado pagina')
        max_page = self.pages()        
        page_number = 1
        page_range = 30 * page_number 
        while self.is_next_present():
            print("papa pa la siguiente")
            time.sleep(3)
            self.open_restaurants(page_number)
            self.goto_next(page_range)
            page_number += 1
            print(page_range)
            time.sleep(3)
            self.open_new_browser()



        # for j in range(1, 43):
        #     min_range = (j-1)*30 if j > 1 else 1
        #     max_range = min_range + 30
        #     for i in range(min_range, max_range):
        #         try:
        #             self.driver.find_element_by_xpath('//*[@id="component_2"]/div/div[%d]/span/div[1]/div[2]/div[1]/div/span/a' %(i)).click()
        #             self.driver.switch_to.window(driver.window_handles[-1])
        #             restaurant = Restaurant(self.driver).get()
        #             print('pagina ' + str(j) + ' restaurante' + str(i))
        #             print(restaurant)
        #             result.append(restaurant)
        #             driver.close()
        #             driver.switch_to.window(driver.window_handles[0])
        #         except:
        #             print("no_funciona")
        #     self.next_page(j+1)
        #     print('hemos pasado de pagina')
        # WebDriverWait(driver, 1).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button.evidon-banner-acceptbutton'))).click()
        return result

if __name__ == "__main__":
    #Opciones de naveragion
    #options = webdriver.ChromeOptions()
    #options.add_argument('--start-maximized')
    #options.add_argument('--disable-extensions')
    #driver_path = 'c:/Users/Michael/Desktop/Python Projects/TripAdvisor Web Scrapper/chromedriver.exe'
    #driver = webdriver.Chrome(driver_path, chrome_options=options)
    driver = webdriver.Chrome()
    myrestaurants = Restaurants(driver).get()
    print(myrestaurants)