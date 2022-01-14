import json
import getpass

email = input("Enter Your GMail: ")
password = getpass.getpass("Enter Your GMail Password: ")
playlistName = input("Enter Your PlayList Name: ")

jsonData = json.dumps({
    "email": email,
    "password": password,
    "playlist-name": playlistName    
}, indent = 4)

with open("user_data.json", "w") as outfile:
    outfile.write(jsonData)