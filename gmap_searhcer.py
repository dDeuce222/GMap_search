import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager




def main():
    if(__name__ == '__main__'):
        chrome_options = uc.ChromeOptions()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

        driver.delete_all_cookies()

        key_file = input("Plz insert keyword file path : ")
        key_file = key_file + '.xlsx' if('.xlsx' not in key_file) else key_file
        df = pd.read_excel(key_file)
        result = []
        for i in range(len(df)):
            row = df.loc[i]
            industry = row[0]
            location = row[1]
            q = industry + '+near+' + location
            url = 'https://www.google.com/maps/search/' + q
            driver.get(url)
            sleep(5)
            places = []
            while(True):
                while(True):
                    try:
                        driver.execute_script("document.getElementsByClassName('kA9KIf')[6].scroll(0,document.getElementsByClassName('kA9KIf')[6].scrollHeight);")
                        break
                    except:
                        sleep(2)
                        continue
                sleep(2)
                if(len(places) == len(driver.find_elements(By.CLASS_NAME , 'THOPZb'))):
                    break
                places = driver.find_elements(By.CLASS_NAME , 'THOPZb')
                
            hrefs = []
            for place in places:
                a_tag = place.find_element(By.TAG_NAME,'a')
                hrefs.append(a_tag.get_attribute('href'))
        
            for href in hrefs:
                driver.get(href)
                sleep(5)
                href = driver.current_url
                name = driver.find_element('xpath' , '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
                current_panel = driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]')
                for div in current_panel.find_elements(By.CLASS_NAME , 'AG25L'):
                    btn = div.find_element(By.TAG_NAME , 'button')
                    item_type = btn.get_attribute('data-item-id')
                    print(div.text)
                    print(btn.text)
                    if(item_type != None):
                        if('address' in item_type):
                            address = div.text
                        elif('phone' in item_type):
                            phone = item_type.replace('phone:tel:','')
                    else:    
                        website = div.find_element(By.TAG_NAME , 'a').get_attribute('href')
                la_index = href.index('@')
                la_end = href.index(',',la_index)
                lo_end  = href.index(',',la_end +1)
                latitude = href[la_index+1:la_end]
                longitude = href[la_end+1:lo_end]
                try:
                    status = current_panel.find_element(By.CLASS_NAME, 'OqCZI').text
                except:                    
                    try:
                        status = current_panel.find_element(By.CLASS_NAME, 'lk1Rcf').text
                    except:
                        status = ''
                f_index = href.index('0x')
                f_end = href.index('!',f_index)
                f_id = href[f_index:f_end]
                rating = driver.find_element('xpath' , '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]').text
                while(True):
                    try:
                        review_counts = driver.find_element('xpath' , '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]').text
                        r_index = review_counts.index(' ')
                        review_counts = review_counts[0:r_index]
                        break
                    except:
                        sleep(1)
                        continue
                keyword = industry + ' ' + location
                try:
                    timing = driver.find_element(By.CLASS_NAME , 'GUrTXd').get_attribute('aria-label')
                except:
                    timing = ''
                category = driver.find_element('xpath' , '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button').text
                reviews = []
                review_divs = []
                sleep(1)
                while(True):
                    try:
                        driver.execute_script("document.getElementsByClassName('kA9KIf')[4].scroll(0,document.getElementsByClassName('kA9KIf')[4].scrollHeight);")
                        break
                    except:
                        sleep(2)
                        continue
                try:
                    driver.execute_script("document.getElementsByClassName('M77dve')[3].click();")
                    sleep(5)
                except Exception as e:
                    print(e)
                while(True):
                    driver.execute_script("document.getElementsByClassName('kA9KIf')[5].scroll(0,document.getElementsByClassName('kA9KIf')[5].scrollHeight);")
                    sleep(2)
                    if(len(review_divs) == len(driver.find_elements(By.CLASS_NAME , 'jftiEf'))):
                        break
                    review_divs = driver.find_elements(By.CLASS_NAME , 'jftiEf')
                
                for div in review_divs:
                    reviewer = div.find_element(By.CLASS_NAME,'d4r55').text
                    try:
                        div.find_element(By.CLASS_NAME , 'kyuRq').click()
                        print(div.find_element(By.CLASS_NAME , 'kyuRq').text)
                        sleep(0.5)
                    except:
                        pass 
                    review_text = div.find_element(By.CLASS_NAME,'MyEned').text
                    reviews.append({'user' : reviewer , 'text' : review_text})
                result.append({
                    'Name' :name,
                    #'GoogleCID' : c_id,
                    'Address' : address,
                    'Phone' : phone,
                    'Latitude' : latitude,
                    'Longitude' : longitude,
                    'Status' : status,
                    'GoogleFID' : f_id,
                    'Rating' : rating,
                    'Reviews' : review_counts,
                    'Review_Texts' : reviews,
                    'Keyword' : keyword,
                    'Timing' : timing,
                    'Category' : category,
                    'Website' : website,
                    'PriceRange' : '',
                    'Result_Type' : 'Organic',
                    'URL' : href,
                })
        
        save_file = input("Save File Name : ")
        save_file = save_file if('.xlsx' in save_file) else save_file + '.xlsx'
        df = pd.DataFrame(result)
        writer = pd.ExcelWriter(save_file,engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Result')
        writer.save()


        

main()
