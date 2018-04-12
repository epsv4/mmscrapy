from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url="http://news.163.com/"
chrome_options = Options()
# specify headless mode
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_page_load_timeout(300)
browser.set_script_timeout(300)
browser.get(url)
title=browser.find_elements_by_xpath('//div[@id="js_top_news"]/h2/a')
print (title[0].get_attribute('innerHTML'))
browser.quit()