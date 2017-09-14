
class Out_path_not_defined(Exception):
    def __init__(self):
        super(Exception, self).__init__('The \'out path\' to expecify the path to write the file is not defined.')

class In_path_not_defined(Exception):
    def __init__(self):
        super(Exception, self).__init__('The \'in path\' to expecify the path to read the file is not defined.')

class Mesage_not_defined(Exception):
    def __init__(self):
        super(Exception, self).__init__('The string with the mesage is not defined.')

class Mesage_too_long(Exception):
    def __init__(self):
        super(Exception, self).__init__('The string with the mesage must be at maximum 1024 bytes.')
