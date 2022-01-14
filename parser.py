from selenium.common.exceptions import NoSuchElementException
import driver_init
import json

#to input data...
import data


# Opening JSON data's file
with open('user_data.json', 'r') as openfile:
    # Reading from json file
    json_data = json.load(openfile)
    
email = json_data['email']
password = json_data['password']
playlistName = json_data['playlist-name']



#getting driver...
driver = driver_init.getDriver()

#go to sign-in page, and sign-in
driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1'+\
'&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
driver.implicitly_wait(15)
driver_init.signIn(driver, email, password)

#go to youtube...
driver.implicitly_wait(30)
driver.refresh()
driver.get('https://www.youtube.com/')

#go to playlist...
driver.find_element_by_xpath('//*[@id ="guide-button"]/button').click()
driver.find_element_by_xpath('//*[@id ="expander-item"]/a').click()

#check if we have that playlist
try:
    playlistButton = driver.find_element_by_xpath(f'//a[@title="{playlistName}"]')
    playlist_found = True
except NoSuchElementException:
    playlist_found = False
    print("No Such Playlist found :(")
    driver.close()

if playlist_found:

    playlistButton.click()

    #getting all video links from playlist...
    videoLinks = []
    videoContainer = driver.find_element_by_xpath('//ytd-playlist-video-list-renderer/div[@id="contents"]')
    allVideos = videoContainer.find_elements_by_xpath(".//ytd-playlist-video-renderer")
    playlistLength = int(driver.find_element_by_xpath("//div[@id='stats']/yt-formatted-string/span").text)

    #load all videos in playlist...
    while len(allVideos) < playlistLength:
        print(len(allVideos))
        lastElement = allVideos[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", lastElement)
        allVideos = videoContainer.find_elements_by_xpath(".//ytd-playlist-video-renderer")

    #get all links...
    for videoElement in allVideos:
        link = videoElement.find_element_by_xpath(".//div[@id='content']/div[@id='container']/div[@id='meta']/h3/a[@id='video-title']").get_attribute("href")
        videoLinks.append(link)

    #write in json file...
    with open("links.json", "w") as outfile:
        outfile.write(json.dumps({ "links": videoLinks }, indent=4))

    print('Data Collected Successfuly!')
    driver.close()










