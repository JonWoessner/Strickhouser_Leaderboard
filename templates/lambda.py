try:
    result=int("li")
except ValueError:
    print('Are you sure')
else:
    pass #Can be used for a success
finally:
    pass #Will activate regardless of success or failure, aka to close a file or window
print('Hey, im still alive')