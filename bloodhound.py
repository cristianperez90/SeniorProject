from selenium import webdriver
import time
from urllib.parse import urlparse
import datetime
import os.path


ads_display_text = []
ads_display_urls = []
ads_aclick_urls = []
new_dir_name = datetime.datetime.now().strftime("%Y_%m_%d-%H%M")
os.mkdir("Results/" + new_dir_name)

def get_results(search_term, num_results=8):
    bing_url = "https://www.bing.com"
    browser = webdriver.Ie(executable_path= 'WebDrivers\Chrome\chromedriver.exe')
    browser.get(bing_url)
    search_box = browser.find_element_by_id("sb_form_q")
    search_box.send_keys(search_term)
    time.sleep(3)
    search_box.submit()
    time.sleep(6)

    try: 
        ad_alinks = browser.find_elements_by_xpath("//div[@class='sb_add sb_adTA' and 1]/h2[1]/a[1]")
        display_urls = browser.find_elements_by_xpath("//div[@class='b_adurl']/cite[1]")
    except zeroResults:
        print("Ad Results: 0")

    for ad in ad_alinks:
        ad_text = ad.text
        ad_aclick_url = ad.get_attribute('href')
        ads_display_text.append(ad_text)
        ads_aclick_urls.append(ad_aclick_url)
    for url in display_urls:
        display_url = url.text
        ads_display_urls.append(display_url)
    browser.close()
    return ads_aclick_urls
    

def search_list(search_terms, num_results = 8):
    for search_term in search_terms:
        results = get_results(search_term, num_results)
    return results

terms_list = open('SearchTerms/SearchTerms.txt').read().splitlines()
search_list(terms_list)


with open('Results/'+ new_dir_name + '/AdData.txt', 'w', encoding='utf-8') as f:
    for (x,y,z) in zip(ads_display_text,ads_display_urls,ads_aclick_urls):
           f.write("Ad Text: {0}\tDisplay URL:{1}\naclick URL:{2}\n\n".format(x,y,z))
    f.close()



for url in ads_aclick_urls:
    filepath = 'Results/'+ new_dir_name
    browser = webdriver.Ie(executable_path= 'WebDrivers\Chrome\chromedriver.exe')
    browser.get(url)
    time.sleep(20)

    website_url = urlparse(browser.current_url)  
    filename = website_url.netloc
    browser.get_screenshot_as_file(os.path.join(filepath, filename + ".png"))
    print("Screenshot saved for: " + filename)
    page_source_path = os.path.join(filepath, filename + ".html")
    page_source = browser.page_source + "\n\n" + url
       
    with open(page_source_path, 'w', encoding='utf-8') as file_object:
        file_object.write(page_source)
        print("Page source saved for: " + filename + "\n")
    browser.close()
