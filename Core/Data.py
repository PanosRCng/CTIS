from Core.IO import IO



class Data:

    __folder = 'data'


    @staticmethod
    def get(filename):
        return IO.path(Data.__folder, filename)

