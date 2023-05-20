import os


class create_init:
    path: str = ""

    def __init__(self, path):
        self.path = path

    def create_init_files(self):
        subdirs = []
        for dirpath, dirnames, filenames in os.walk(self.path):
            for dirname in dirnames:
                subdirs.append(os.path.join(dirpath, dirname))

        for subdir in subdirs:
            new_init_file_path = os.path.join(subdir, '__init__.py')
            if not os.path.exists(new_init_file_path):
                init_file = open(os.path.join(subdir, '__init__.py'), 'w')
                init_file.write('')
                init_file.close()
