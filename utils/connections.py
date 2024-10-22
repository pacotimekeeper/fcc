import requests

SESSION = requests.Session()

def login() -> int:
    print("Loggin in with credentials...")
    data = {"username":"paco",
            "password":"1234",
            "Submit":"Login"}
    url = "http://fcc/fcc/login.php?act=login"
    response = SESSION.post(url, data=data)
    if response.status_code != 200: return
    print("You are logged in.")

def has_permission(url: str) -> bool:
    response = SESSION.get(url)
    result = response.text
    return result != "No permissions" ## No permission -> False