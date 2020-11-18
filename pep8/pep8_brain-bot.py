#Author: Brian Wu
#
# change_calculator.py
#
# Last Editied: 2020-11-18
#
# Purpose:
#
# This script will take a positive integer as input
# and determine the number of quarters, dimes, nickels, and pennies
# needed to obtain this exact number of cents, using as few contains
# as possible.
#
###########
# MODULES #
###########
import argparse
##############################
# Calculate coin combination #
##############################
def change(amount):
    """Calculates the number of each coin that'll be needed for the combination of coins
    to get the exact input in cents.
    Basically, this function calculates the simplest way to generate
    exact change using common American coins.

    parameter: amount -- number of cents"""
    if amount < 0:
        raise ValueError('It\'s impossible to have a negative number of cents. Please try again.')
    # The amount can't be negative
    #
    coin_counter = dict();
    # This dictionary keeps track of the number of each American coin
    #
    quarters = int(amount/25)
    amount -= (quarters*25)
    dimes = int(amount/10)
    amount -= (dimes*10)
    nickels = int(amount/5)
    amount -= (nickels*5)
    pennies = amount

    coin_counter['Quarters'] = quarters
    coin_counter['Dimes'] = dimes
    coin_counter['Nickels'] = nickels
    coin_counter['Pennies'] = pennies
    return coin_counter

#############
#   Main    #
#############
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the combination of the'
                                    ' smallest number of common American coins (quarters, dimes, nickels, and pennies)'
                                    ' that add up to the given number of cents. The number of cents needs to be'
                                    ' represented by an integer and must be positive.')
    parser.add_argument('amount', type=int,
                        help="The total number of cents (integer)")
    args = parser.parse_args()
    print("The number of quarters, dimes, nickels, and pennies needed to ",
        "generate exact change: \n", change(args.amount))
