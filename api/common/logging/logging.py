from datetime import datetime 

class Log:

    def __init__(self):
        self.__colors = {
            "red": "\033[1;31m",
            "blue": "\033[96m",
            "yellow": "\033[93m",
            "white": "\33[37m"
        }

        self.__time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")        

    def __fetch_args(self, arguments):
        return "".join(["{}".format(a) for a in arguments])
 
    def error(self, *args) -> None:
        print(f"{self.__colors['red']}[{self.__time}] ERROR:", f"{self.__colors['white']}{self.__fetch_args(args)}")

    def info(self, *args) -> None:
        print(f"{self.__colors['blue']}[{self.__time}] INFO:",  f"{self.__colors['white']}{self.__fetch_args(args)}")

    def warning(self, *args) -> None:
        print(f"{self.__colors['yellow']}[{self.__time}] WARNING:", f"{self.__colors['white']}{self.__fetch_args(args)}")


log = Log()