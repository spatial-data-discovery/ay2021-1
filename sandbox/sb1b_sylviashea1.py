import math
import sys

def main():
    # User input
    sys.stdout.write('Enter a number between -180 and 180: ')
    sys.stdout.flush()
    # Split user number
    nums = math.modf(float(input()))
    # Get a
    a = int(nums[1])
    # Get b
    preb = math.modf(nums[0]*60)
    b = int(math.floor(preb[1]))
    # Get c
    c = preb[0]*60
    print('a =', a,'b =',b,'c =',c)

if __name__=='__main__':
    main()
