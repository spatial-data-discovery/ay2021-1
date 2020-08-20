from numpy import math


# Define the function for sandbox problem B

def sandbox_b(Y):
    pieces = math.modf(Y) # split the integer part from the decimal
    
    # get value for part a
    a = pieces[1]
    
    # get value for part b
    deci_part = pieces[0]
    b = deci_part*60 
    deci_part = math.modf(b)
    b = int(b) # round down with int()

    # calculate part c
    second_deci = deci_part[0]
    c = second_deci*(60**2) 

    #re-calculate the user's value. NOTE: it should be a bit different b/c of rounding
    to_return = a + (1/60)*b + (1/60**2)*c 
    print('Original input was: ', Y,'\nPost-script we have: ', to_return)



i=0
while i==0:
    user_number = input('Input a number between -180 and 180')
    user_number=float(user_number)
    if user_number < 180 and user_number > -180:
        sandbox_b(user_number)
        i=1
    else:
        print('Invalid input. Try again.')
