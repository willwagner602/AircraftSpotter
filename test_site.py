from selenium import webdriver

development = "http://127.0.0.1"
production = "http://www.willwagner.me"

driver = webdriver.Chrome()
driver.get(development)

navbar = driver.find_element_by_id("navbar")
print(navbar)

driver.quit()