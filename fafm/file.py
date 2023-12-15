import os


class File():
    filename = ''
    '''
    open_modes
    r = read (default)
    w = write (truncate if exists)
    x = create new and open for write
    a = append to the end if file exists
    b = binary mode
    t = text mode (default as r)
    + = open a disk file for updating (read and write)
    U = universal newline mode (deprecated)
    '''
    open_modes = (
        'r', 'w', 'x', 'a', 'b', 't', '+', 'U'
    )

    def __init__(self, filename, auto_create_file=False) -> None:
        self.filename = filename
        self.check_file_path()
        if auto_create_file:
            if not self.exists():
                self.write('', 'x')
        
    def check_file_path(self):
        if self.filename.find('/') == -1:
            self.filename = os.path.join(os.getcwd(), self.filename)
        
    def teste(self):
        return self.filename

    def exists(self, thefile=''):
        x = thefile if thefile != '' else self.filename
        return True if os.path.isfile(x) else False
    
    def get_file_mode(self, mode):
        for m in self.open_modes:
            if mode == m:
                return mode 
        raise Exception(f'File.get_file_mode({mode}) is not valid file mode')

    def read(self):
        ret = []
        if not self.exists():
            return ret
        with open(self.filename, 'r') as f:
            ret.append(f.readlines())
        return ret

    def write(self, content, mode='a'):
        m = self.get_file_mode(mode)
        with open(self.filename, m) as f:
            f.write(content)
        f.close()

    def delete(self, file_with_path=''):
        x = file_with_path if file_with_path != '' else self.filename
        if self.exists(x):
            os.remove(x)


class_file_comments = '''
exemplo de uso 
file = File('teste.txt')
file.delete()

i = 0
for i in range(1, 10):
    now = str(datetime.datetime.now())
    i += 1
    file.write('fafm teste ' + now + ' = ' + str(i) + "\n")

print(file.read())

'''
