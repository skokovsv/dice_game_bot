


from selenium import webdriver

driver = webdriver.Chrome()


driver.get("")

driver.save_screenshot("you.png")
driver.quit()