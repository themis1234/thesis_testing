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
        violations_local = []
        viol_dict = {}
        while(line != "END_VIOLATIONS"):
            if(not line.startswith("\n")):
                line = line.strip(" \n")
                splited = line.split(':')
                viol_dict[splited[0]] = splited[1]   
            else:
                violations_local.append(viol_dict)
                viol_dict = {}
            line = f.readline()
        self.violations = self.sortViolationsBasedOnAttribute(violations_local)
        print(self.violations)

        
    @staticmethod  
    def sortViolationsBasedOnAttribute(violations):
        violationsByAttribute = {}
        for item in violations:
            attribute = item["ATTRIBUTES"]
            violation = item["ACTION"]
            if(attribute in violationsByAttribute):
                violationsByAttribute[attribute].append(violation)
            else:
                violationsByAttribute[attribute] = [violation]
        return violationsByAttribute

    def checkForViolation(self, filename):
        f = open(filename)
        line_number = 1
        line = f.readline()
        database = self.database
        violations = []
        while(len(line) != 0):
            if(line.find("requests") != -1  and not line.startswith("import")): #Finds database, checks for get requests
                parts = line.split("requests")
                if(line.find(database) != -1):
                    if(parts[1].startswith(".get")):
                        url = re.search("(?P<url>https?://[^\s]+)",parts[1]).group("url").strip("')") #Finds the url in the line. Problem when in the same line as the url is a /
                        data = self.urlGETHandler(url)
                        print(data)
                        print(url)
                        for attribute in data:
                            print(attribute)
                            if("GET" in self.violations[attribute]):
                                violations.append(attribute + " GET in line " + str(line_number))
                    elif(parts[1].startswith(".put")):
                        data = self.urlPUTHandler(parts[1])
                        if(data and "PUT" in self.violations[data]):
                            violations.append(attribute + " PUT in line " + str(line_number))

                else:
                    request = parts[1]
                    test = self.postRequestHandler(parts[1], self.violations)
                    if(test):
                        violations.append(test + " in line " + str(line_number))

            line_number += 1  
            line = f.readline()
        print(violations)

    @staticmethod
    def postRequestHandler(request, violations):
        data = request.split("=")[1].strip(" )\n")
        print(data)
        func = request.split("(")[0]
        if(data in violations and violation_to_function[func] in violations[data]):
            return data + " " + violation_to_function[func]
        return False


    # def checkIfDataHaveViolation(self, data):
    #     violations = set()
    #     for attribute in data:
    #         if(attribute in self.violations):
    #             violations.add(self.violations[attribute][0])
                
    #     return violations
            

    def urlGETHandler(self, url):
        parts = url.split("?")
        if(len(parts) != 1):
            database = parts[0]
            variables = parts[1]
            print(variables, 1234)
            if(database == self.database and variables.startswith("columns=")):
                variables = variables[8:] #removes "columns="
                data = variables.split(",")
                return data #returns the data that the GET request asked for
            else: return False

    
    def urlPUTHandler(self, request):
        data = request.split(",")[1].split("=")[0].strip(" ")
        if(data in self.violations):
            return data
        return False



test = violationHandler("Violations", "https://www.myawesomedbservice.com/api/database")

test.findVioaltions()
test.checkForViolation("testing.py")