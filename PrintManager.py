SPLIT_LINE_LEN = 20

class PrintManager:
    __last_print_line_len = 0
    def clear_line(self):
        print(" " * self.__last_print_line_len, end="\n")
    def line(self, str_to_print, new_line = False):
        spaces = ''
        if self.__last_print_line_len > len(str_to_print):
            spaces = ' ' * (self.__last_print_line_len - len(str_to_print))
        print(str_to_print, spaces, end= "\r" if not new_line else "\n")
        self.__last_print_line_len = len(str_to_print)
    def on_line(self, *argv):
        str_to_print = " ".join([str(i) for i in argv])
        self.line(str_to_print, False)
    def new_line(self, *argv):
        str_to_print = " ".join([str(i) for i in argv])
        self.line(str_to_print, True)
    def splitter(self):
        self.new_line('-' * SPLIT_LINE_LEN)
    def title(self, title):
        title_len = len(title)
        add_one_splitter = not bool(int(title_len/2))
        title_splitter = '-' * int((SPLIT_LINE_LEN - len(title))/2)
        str_to_print = title_splitter
        str_to_print += title
        str_to_print += title_splitter
        if add_one_splitter:
            str_to_print += '-' 
        self.new_line(str_to_print)
    def print_file(self, file_path):
        with open(file_path, 'r') as f:
            print(f.read())


#colors - https://www.geeksforgeeks.org/print-colors-python-terminal/
class bcolors:
    red='\033[31m'
    yellow='\033[93m'
    purple='\033[35m'
    lightblue='\033[94m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'