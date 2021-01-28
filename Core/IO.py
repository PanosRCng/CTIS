import os



class IO:


    @staticmethod
    def path(folder, datafile):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), '../' + folder + '/' + datafile)


    @staticmethod
    def files_in_directory_tree(directory_path):

        dir_files = os.listdir(directory_path)

        files = []

        for file in dir_files:

            file_path = os.path.join(directory_path, file)

            if os.path.isdir(file_path):
                files = files + IO.files_in_directory_tree(file_path)
            else:
                files.append(file_path)

        return files

