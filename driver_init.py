from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def getDriver():
    return webdriver.Chrome(ChromeDriverManager().install())

def signIn(driver, email, password):
    
    #email...
    loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
    loginBox.send_keys(email)

    nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
    nextButton[0].click()

    #password...
    passWordBox = driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div/div[1]/input')
    passWordBox.send_keys(password)

    nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
    nextButton[0].click()