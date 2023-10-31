class FileWriter:
    def __init__(self, filename):
        self.filename = filename
    
    def clear_file(self):
        with open(self.filename, 'w') as file:
            file.truncate(0)
    
    def write_to_file(self, content):
        with open(self.filename, 'a') as file:
            file.write(content + '\n')