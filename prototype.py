import numpy as np
import re

violation_to_function = {
    ".get" : "GET", ".post" :"POST", ".put": "PUT", ".delete": "DELETE"
}

class violationHandler:
    def __init__(self, violation_text, database):
        self.violation_text = violation_text
        self.database = database
        self.violations = []


    def findVioaltions(self):
        f = open(self.violation_text, "r")
        line = f.readline()
        viol_dict = {}
        while(line != "END_VIOLATIONS"):
            if(not line.startswith("\n")):
                line = line.strip(" \n")
                splited = line.split(':')
                viol_dict[splited[0]] = splited[1]   
            else:
                self.violations.append(viol_dict)
                viol_dict = {}
            line = f.readline()

    def checkForViolation(self, filename):
        f = open(filename)
        line = f.readline()
        database = self.database
        while(len(line) != 0):
            if(line.find(database) != -1):
                parts = line.split("requests")
                if(len(parts) != 1):
                    url = re.search("(?P<url>https?://[^\s]+)",parts[1]).group("url").strip("')") #Finds the url in the line 
                    data = self.urlhandler(url)
                    print(url)
                    violations = self.checkIfDataHaveViolation(data)
                    print(violations)
                    # for key in violation_to_function.keys():
                    #     if(parts[1].startswith(key)):
                            # pass
            line = f.readline()

    def checkIfDataHaveViolation(self, data):
        violations = set()
        for attribute in data:
            for violation in self.violations:
                if(attribute == violation["ATTRIBUTES"]):
                    violations.add(violation["ACTION"])
                    break
        return violations
            


    def urlhandler(self, url):
        parts = url.split("?")
        if(len(parts) != 1):
            database = parts[0]
            variables = parts[1]
            if(database == self.database and variables.startswith("columns=")):
                variables = variables[8:] #removes "columns="
                data = variables.split(",")
                return data
            else: return False


test = violationHandler("Violations", "https://www.myawesomedbservice.com/api/database")

test.findVioaltions()
test.checkForViolation("testing.py")