"""
This library webscrap hotel reviews from tripadvisor.com and save it into a csv file.
Done by frostsg
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def setupChrome():
    """This is a function to setup the webdriver to use chrome for automation"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver is setup using this arguments
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    return driver

def NEW_tripadvisor_ExtractReview(url):
    """This is a function to extract hotel reviews from tripadvisor with the url of a specific hotel as an argument."""
    # Webdriver is being setup to use chrome
    webdriver = setupChrome()
    # webdriver is going to website via url
    webdriver.get(url)
    # Hotel name is extracted and saved into hotel_name
    hotel_name = webdriver.find_element(By.ID, value="HEADING").text
    # Description of hotel is extracted and saved into variable hotel_description
    hotel_description = webdriver.find_element(By.CSS_SELECTOR, value=".fIrGe._T").text
    # Address of hotel is extracted and saved into variable hotel_address
    hotel_address = webdriver.find_element(By.CSS_SELECTOR, ".fHvkI.PTrfg").text
    # A new csv file is created with these few headings
    #df = pd.DataFrame(columns = ['address', 'name', 'reviews.text', 'reviews.rating'])
    df = pd.read_csv("Filtered_Datafiniti_Hotel_Main_Review.csv")
    print(len(df))
    # A for loop that will loop 20 times
    for j in range(0,20):
        time.sleep(2)
        # webdriver to get review boxes and put it in a list
        review_box = webdriver.find_elements(By.XPATH, "//div[@data-reviewid]")
        #rating = webdriver.find_elements(by=By.XPATH, value="//span[contains(@class,'ui_bubble_rating bubble_')]")
        # Looping through the list of review boxes
        for i in review_box:
            # find the review 
            review = i.find_element(by=By.CSS_SELECTOR, value='.fIrGe._T').text 
            # save the title, date and review into csv file
            df.loc[len(df)] = [hotel_address, hotel_name, review, ' ']        
        try:
            webdriver.find_element(By.XPATH, "//a[@class='ui_button nav next primary ']").click()
        except ElementClickInterceptedException:
            break
    # replacing the spaces in hotel_name with _
    hotel_name = hotel_name.replace(" ", "_")
    # Updating the CSV file 
    df.to_csv("Filtered_Datafiniti_Hotel_Main_Review.csv", index=False)
    # Stopping the webdriver
    webdriver.quit()

def urlchecker(url):
    """This function is used to check the url to see which hotel website it is being used."""
    # If airbnb is being used, then airbnb extract function is used
    if "airbnb" in url:
        print("Feature is coming soon!")
        #airbnb_ExtractReview(url)
    # If tripadvisor is being used, then tripadvisor extract function is used
    elif "tripadvisor" in url:
        NEW_tripadvisor_ExtractReview(url)
    # If booking is being used, then booking extract function is used
    elif "booking" in url:
        print("This feature is coming soon")
        #booking_ExtractReview(url)
    else:
        print("This url is invalid")
          
          

#urlchecker("https://www.tripadvisor.com/Hotel_Review-g298570-d555433-Reviews-Hilton_Kuala_Lumpur-Kuala_Lumpur_Wilayah_Persekutuan.html")
#urlchecker("https://www.tripadvisor.com.sg/Hotel_Review-g298570-d12621892-Reviews-EQ_Kuala_Lumpur-Kuala_Lumpur_Wilayah_Persekutuan.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g60763-d93525-Reviews-Sanctuary_Hotel_New_York-New_York_City_New_York.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g194856-d498287-Reviews-Hotel_Balocco-Porto_Cervo_Arzachena_Province_of_Olbia_Tempio_Sardinia.html")
#urlchecker("https://www.tripadvisor.com.sg/Hotel_Review-g294265-d302294-Reviews-Pan_Pacific_Singapore-Singapore.html")
#urlchecker("https://www.tripadvisor.com/Hotel_Review-g294265-d301468-Reviews-or3905-Mandarin_Oriental_Singapore-Singapore.html")

