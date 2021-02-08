from datetime import datetime


class Logger:


    @staticmethod
    def log(source, message, type='info'):

        if type == 'info':
            print(Logger.time_stamp() + "\tINFO\t: " + source + ",\t" + message)
        elif type == 'warning':
            print(Logger.time_stamp() + "\tWARNING\t: " + source + ",\t" + message)
        elif type == 'error':
            print(Logger.time_stamp() + "\tERROR\t: " + source + ",\t" + message)


    @staticmethod
    def time_stamp():
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


