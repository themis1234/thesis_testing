import requests 


def getPassword(url):
    passwords = requests.get('https://www.myawesomedbservice.com/api/database?columns=passwords')
    return passwords
