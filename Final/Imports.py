import ast
import os


class Imports():
    
    def __init__(self, path) :
        self.imports = self.map_imports(path)
        self.directory = path
    
    @staticmethod
    def parse_imports(filepath):
        with open(filepath, "r") as file:
            tree = ast.parse(file.read())
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name + ".py" for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:  # ignore relative imports for simplicity
                        imports.append(node.module + ".py")
            return imports

    def map_imports(self, directory):
        import_map = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    imports = self.parse_imports(full_path)
                    import_map[file] = imports
        return import_map
    
    def findFileDependancies(self, filename, dependencies = set()):
        if self.imports.get(filename, "Last Node") != "Last Node":
            dependencies.update(self.imports[filename])
            for file in self.imports[filename]:
                self.findFileDependancies(file, dependencies=dependencies)

        return dependencies
    
    def getRelativeCode(self, filename):
        file_list = self.findFileDependancies(filename)
        file_list.add(filename)
        full_text = ""  # Initialize an empty string to hold the concatenated text
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file in file_list:
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r') as file:  # Open the file
                        full_text += f"The definition of file {file} is:\n" + file.read() + "\n\n"  # Read the file and append its content to full_text
        return full_text  # Return the concatenated string
        
    


# project_directory = 'testing_repo'  # Set your project directory here

# imports = Imports(project_directory)
# imports_dictionary = imports.imports
# # dependencies = imports.findFileDependancies("file4")
# print(imports.getRelativeCode("file4.py"))
