LOWER_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', ' ']
UPPER_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z', ' ']

NUMERIC = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
ALPHA_NUMERIC = LOWER_ALPHABET[:-1] + UPPER_ALPHABET[:-1] + NUMERIC[:-1] + [' ']
SPECIAL_CHAR = ['!','"', '$', '%','^','&','*','(',')','-','_','=','+','{','}','[',']','#','~','@',"'",';',':','/','?',
                '>','.',',','<','|']
ALL_CHAR = ALPHA_NUMERIC + SPECIAL_CHAR