import string
import random
stringLength=8
lettersAndDigits = string.ascii_letters + string.digits
t= ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
print(t)
