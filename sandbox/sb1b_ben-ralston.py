user_input = input('Please enter a number between -180 and 180: ')
while True:
    try:
        user_number = float(user_input)
        if -180 <= user_number <= 180:
            break
    except ValueError:
        pass
    user_input = input('That is not a valid input. Please try again: ')

negative = user_number < 0
if negative:
    user_number *= -1

integer, remainder = int(user_number), user_number % 1
sixtieths = int(remainder // (1/60))
remainder_2 = remainder - sixtieths / 60
sixtieths_squared = int(remainder_2 // (1/60**2))

if not negative:
    expression = '%f = %i + (1/60)*%i + (1/60^2)*%i' % (user_number, integer,
                                                        sixtieths, sixtieths_squared)
else:
    expression = '%f = %i - (1/60)*%i - (1/60^2)*%i' % (user_number, integer,
                                                        sixtieths, sixtieths_squared)
print(expression)
