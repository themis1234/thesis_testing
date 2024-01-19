import inspect

class NewList():
    def __init__(self, data):
        self.data = data
        self.possible_vulnerabilities = []

    def __getitem__(self, index):
        if(index == 0):
            f = inspect.currentframe()
            i =  inspect.getframeinfo(f.f_back)
            self.possible_vulnerabilities.append(i)
        return self.data[index]
    
    


    