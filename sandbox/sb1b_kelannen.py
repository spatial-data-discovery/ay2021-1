import math

user_float = float(input('Please enter a number between -180 and 180: '))
while user_float < -180 or user_float > 180:
    user_float = float(input('Please enter a number between -180 and 180: '))

float_seperated = math.modf(user_float)

a = float_seperated[1]

b = math.floor(float_seperated[0] * 60)

c = math.modf(float_seperated[0] * 60)[0]*(60**2)

print(user_float, "=", a, "+ (1/60) *",b,"+ (1/60^2) *",c)