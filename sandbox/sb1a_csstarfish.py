import math

num_out_of_range = True
while num_out_of_range:
    user_input = input("Enter a number between -180 and 180: ")
    user_num = float(user_input)

    if user_num >= -180 and user_num <= 180:
        num_out_of_range = False


a = int(user_num)
b = math.floor((user_num/60))
c = user_num/(60**2)

print("\nInteger portion of number: " + str(a))
print("Number expressed in sixtieths and rounded down to the nearest whole number: " + str(b))
print("Number expressed in sixtieths of a sixtieth: " + str(c))

# This calculation and print statement were used to test the accuracy of the calculations for a, b, and c.
num = a + (1/60)*b + (1/(60**2))*c
print("\nOriginal number: " + str(user_num) + ", Calculated number: " + str(num)) 