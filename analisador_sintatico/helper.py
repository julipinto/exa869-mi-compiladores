def is_type(token):
    return token in ['int', 'real', 'boolean', 'string']

def is_logical(token):
    return token in ['&&', '||']

def is_boolean(token):
    return token in ['true', 'false']

def red_painting(word): 
    #painting a word in red on terminal
    return '\033[1;31m' + str(word) + '\033[0;0m'

def blue_painting(word): 
    #painting a word in blue on terminal
    return '\033[1;34m' + str(word) + '\033[0;0m'

def print_if_missing_expecting(expecting_stack):
    if(len(expecting_stack) > 0):
        expecting_stack.reverse()
        print('Error: missing tokens ' + str(expecting_stack))

def create_stack(arr):
    arr.reverse()
    return arr
