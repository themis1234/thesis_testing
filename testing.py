import requests 


def getPassword():
    passwords = requests.get('https://www.myawesomedbservice.com/api/database?columns=passwords')
    return passwords

# def postEmail(emails):
#     requests.post('https://www.anyurl.com' , json = email)
