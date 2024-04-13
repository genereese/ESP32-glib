
class Logger:
    """ Simple logging object for debugging and console information """

    def __init__(self, level=1):
        self.levels = {"ERROR": 1, "INFO": 2, "DEBUG": 3}
        self.current_level = level
    
    def setLevel(self, level):
        self.current_level = level
    
    def log(self, message, level="INFO"):
        if self.levels[level] <= self.current_level:
            print(f"{level}: {message}")

    def error(self, message):
        self.log(message, "ERROR")
    
    def info(self, message):
        self.log(message, "INFO")
    
    def debug(self, message):
        self.log(message, "DEBUG")
