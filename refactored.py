from selenium import webdriver
import os.path
import time
from urllib.parse import urlparse
import datetime

ads_display_text = []
ads_display_urls = []
ads_aclick_urls = []


def create_directory():
    directory_name = datetime.datetime.now().strftime("%Y_%m_%d-%H%M")
    os.mkdir("Results/" + directory_name)
    directory = "Results/" + directory_name
    return directory

def select_browser():

    print("Please select the browser for crawl: \n\t[1] Chrome\n\t[2] Edge\n\t[3] Firefox\n\t[4] IE\n\t[5] PhantomJS")
    browser = input()
    if browser == "1":
        browser = webdriver.Chrome(executable_path = 'WebDrivers\Chrome\chromedriver.exe')
        return browser
    elif browser =="2":
        browser = webdriver.Edge(executable_path = 'WebDrivers\Edge\MicrosoftWebDriver.exe')
        return edge
    elif browser == "3":
        browser = webdriver.Firefox(executable_path = 'WebDrivers\Firefox\geckodriver.exe')
        return browser
    elif browser == "4":
        browser =  webdriver.PhantomJS(executable_path = 'WebDrivers\PhantomJS\bin\phantomjs.exe')
        return browser
    else: select_browser()


def select_search_list():
    print("Provide full path to txt file containing search terms\nSearch terms must be delimited by a new line")
    file_path = input("Path: ")
          
    terms_list = open(file_path).read().splitlines()
    return terms_list


def select_ad_elements(browser):
    ad_links = browser.find_elements_by_xpath("//div[@class='sb_add sb_adTA' and 1]/h2[1]/a[1]")
    display_urls = browser.find_elements_by_xpath("//div[@class='b_adurl']/cite[1]")
    
    for ad in ad_links:
        ads_display_text.append(ad.text)
        ads_aclick_urls.append(ad.get_attribute('href'))
    for url in display_urls:
        ads_display_urls.append(url.text)


def save_ad_info(directory):
    with open(directory + '/AdData.txt', 'w', encoding='utf-8') as f:
        for (x,y,z) in zip(ads_display_text,ads_display_urls,ads_aclick_urls):
               f.write("Ad Text: {0}\tDisplay URL:{1}\naclick URL:{2}\n\n".format(x,y,z))
        f.close()

def save_screenshot(browser, directory, filename):
    browser.get_screenshot_as_file(os.path.join(directory, filename +".png"))


def save_html(browser, directory, filename, ad_url):
    html_path = os.path.join(directory, filename + ".html")
    page_source = browser.page_source + "\n\nAd URL: " + ad_url
    with open(html_path, 'w', encoding='utf-8') as file_object:
        file_object.write(page_source)
            

def crawl_ads(browser, directory):
    for ad_url in ads_aclick_urls:
        browser.get(ad_url)
        time.sleep(10)
        landing_url = urlparse(browser.current_url)
        filename = landing_url.netloc
        save_screenshot(browser, directory, filename)
        save_html(browser, directory, filename, ad_url)


def execute_search_query(browser, search_term, directory):
    bing_url = "https://www.bing.com"
    browser.get(bing_url)
    search_box = browser.find_element_by_id("sb_form_q")
    search_box.send_keys(search_term)
    time.sleep(3)
    search_box.submit()
    time.sleep(6)
    select_ad_elements(browser)
    save_ad_info(directory)    


def start_search(browser, search_list, directory):
     for search_term in search_list:
        execute_search_query(browser,search_term, directory)
    

def start_crawl():
    directory = create_directory()
    browser = select_browser()
    search_list = select_search_list()
    start_search(browser, search_list, directory)
    crawl_ads(browser, directory)
    browser.close()

    

start_crawl()