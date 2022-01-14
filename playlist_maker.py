import driver_init
import json
import getpass

# Opening JSON links file
with open('links.json', 'r') as openfile:
    json_data = json.load(openfile)
links = json_data['links']

email = input("Enter Your Another GMail: ")
password = getpass.getpass("Enter Your Another GMail Password: ")
playlistName = input("Enter PlayList Name: ")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--lang=en");
prefs = {
  "translate_whitelists": {"ru":"en"},
  "translate":{"enabled":"true"}
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)

#go to sign-in page, and sign-in
driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1'+\
'&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
driver.implicitly_wait(15)
driver_init.signIn(driver, email, password)
driver.implicitly_wait(30)
driver.refresh()

def page_has_loaded():
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

for link in links:
    
    driver.get(link)
    
    if page_has_loaded():
        
        driver.find_element_by_link_text("SAVE").click()   
        playlists = driver.find_elements_by_xpath('//div[@id="playlists"]/ytd-playlist-add-to-option-renderer')

        not_found = True
        for playlist in playlists:
            checkbox = playlist.find_element_by_xpath('.//tp-yt-paper-checkbox')
            playlist_text = checkbox.find_element_by_xpath('.//div[@id="checkboxLabel"]/div[@id="checkbox-container"]/div[@id="checkbox-label"]/yt-formatted-string').text

            if playlist_text == playlistName:
                not_found = False
                if checkbox.get_attribute('aria-checked') == "false":
                    checkbox.click()
                    driver.implicitly_wait(500)
                    break
                
        if not_found:
            driver.find_element_by_xpath('//div[@id="actions"]/ytd-add-to-playlist-create-renderer/ytd-compact-link-renderer/a').click()
            driver.find_element_by_xpath('//div[@id="labelAndInputContainer"]/iron-input/input').send_keys(playlistName)
            driver.find_element_by_xpath('//div[@id="actions"]/ytd-button-renderer/a').click()
        
        driver.implicitly_wait(500)   
    
print("Done...")    
driver.close()