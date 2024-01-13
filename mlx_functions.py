import requests, hashlib
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.firefox.options import Options
from env import *

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def signin():
    url = "https://api.multilogin.com/user/signin"
    payload = {
        "email": f"{mlx_email_address}",
        "password": hashlib.md5(mlx_password.encode()).hexdigest()
    }
    r = requests.post(url=url, headers=HEADERS, json=payload)
    if r.status_code != 200:
        print("Wrong credentials")
    else:
        json_response = r.json()
        token = json_response['data']['token']
        return token

def start_profile():
    #folder_id, profile_id, browser_type = get_profile_id()
    token = signin()
    HEADERS.update({
        "Authorization": f"Bearer {token}"
    })
    url = f"https://launcher.mlx.yt:45001/api/v1/profile/f/{folder_id}/p/{profile_id}/start?automation_type=selenium&headless_mode=false"
    r = requests.get(url=url, headers=HEADERS)
    if r.status_code != 200:
        print("Unable to start profile")
    else:
        json_response =  r.json()
        profile_port = json_response['status']['message']
        print(f"profile port is {profile_port}")
        return profile_port, profile_id, browser_type
    
def stop_profile(profile_id):
    token = signin()
    HEADERS.update({
        "Authorization": f"Bearer {token}"
    })
    url = f"https://launcher.mlx.yt:45001/api/v1/profile/stop/p/{profile_id}"
    r = requests.get(url=url, headers=HEADERS)
    if r.status_code != 200:
        print("Can't stop profile")
    else:
        print("Profile stopped")

def get_folder_id():
    token = signin()
    HEADERS.update({
        "Authorization": f"Bearer {token}"
    })
    url = "https://api.multilogin.com/workspace/folders"
    r = requests.get(url=url, headers=HEADERS)
    json_response = r.json()
    folders = json_response['data']['folders']
    print("\nChoose the folder: \n")
    for i, folder in enumerate(folders, start=0):
        print(f"{i}. {folder['name']}")
    chosen_folder = int(input("\nWhat is the number of the folder you want?\n"))
    folder_id = folders[chosen_folder]['folder_id']
    print(f"\nFolder name: '{folders[chosen_folder]['name']}' | Folder ID: '{folder_id}'\n")
    return folder_id

def get_profile_id():
    folder_id = get_folder_id()
    url = "https://api.multilogin.com/pss/search"
    token = signin()
    HEADERS.update({
        "Authorization": f"Bearer {token}"
    })
    payload = {
        "is_removed": False,
        "limit": 100,
        "offset": 0,
        "search_text": "",
        "storage_type": "all",
        "folder_id": f"{folder_id}",
        "tags": [],
        "order_by": "created_at",
        "sort": "asc"
    }
    r = requests.post(url=url, headers=HEADERS, json=payload)
    json_response = r.json()
    profiles_in_folder = json_response['data']['profiles']
    print("\nChoose the profile you want to use:\n")
    for i,profile in enumerate(profiles_in_folder, start=0):
        print(f"{i}. {profile['name']}")
    chosen_profile = int(input("\nWhat is the number of the profile you want to use?\n"))
    profile_id = profiles_in_folder[chosen_profile]['id']
    browser_type = profiles_in_folder[chosen_profile]['browser_type']
    print(f"\nProfile name: '{profiles_in_folder[chosen_profile]['name']}'\nProfile ID: '{profile_id}'\nBrowser type: '{browser_type}'")
    return folder_id, profile_id, browser_type

def instantiate_driver():
    profile_port, profile_id, browser_type = start_profile()
    if browser_type == 'mimic':
        driver = webdriver.Remote(command_executor=f"http://127.0.0.1:{profile_port}", options=ChromiumOptions())
    elif browser_type == 'stealthfox':
        driver = webdriver.Remote(command_executor=f"http://127.0.01:{profile_port}", options=Options())
    return driver, profile_id
