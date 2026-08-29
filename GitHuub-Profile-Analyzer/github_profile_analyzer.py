from h11 import Data
import requests

username = input("Enter GitHub username: ")
url = f"https://api.github.com/users/{username}"

response = requests.get(url)

if response.status_code == 200:
    udata = response.json()

    print("\n== GitHub Profile Information ===")
    print(f"Name: {udata.get('name')}")
    print(f"Username: {udata.get('login')}")
    print(f"Bio: {udata.get('bio')}")
    print(f"Public Repositories: {udata.get('public_repos')}")
    print(f"Followers: {udata.get('followers')}")
    print(f"Following: {udata.get('following')}")
    print(f"Location: {udata.get('location')}")
    print(f"Profile URL: {udata.get('html_url')}")

else:
    print(f"Error: Unable to fetch data for username '{username}'. Status code: {response.status_code}")