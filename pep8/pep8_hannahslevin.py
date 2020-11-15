#PEP 8 Script
#
#Hannah Slevin
#
#PEP8.py
#
#VERSION 1.0
#
#LAST EDIT: 2020-11-14
#
#The program will collect each percentage grade and turn them into points that
#sum up to 100 and output a final percentage and letter grade for the course.
#
#######################
#  REQUIRED MODULES   #
#######################
#
import argparse
#
############################
# Calculating Letter Grade #
############################
#Calculate letter grade based on grade distribution found in syllabus using a
#series of if statements
#If the user scores over 93%, print A & a message
def LetterGrade(total_pcnt):
    """Calculate the final letter grade.

    Keyword arguments:
    total_pcnt -- the percentage grade calculated in the main frame
    """
    try:
        total_pcnt = float(total_pcnt)
    except:
        raise TypeError("Value must be input as an integer or float! Try again.")
    if total_pcnt > 93.0:
        print("Final Letter Grade: A")
        print("Congratulations on Superior Mastery!")
    #If the user scores between 90% and 92.99%, print A-
    elif (total_pcnt >= 90) & (total_pcnt <= 92.99):
        print("Final Letter Grade: A-")
    #If the user scores between 87% and 89.99%, print B+
    elif (total_pcnt >= 87) & (total_pcnt <= 89.99):
        print("Final Letter Grade: B+")
    #If the user scores between 83% and 86.99%, print B & a message
    elif (total_pcnt >= 83) & (total_pcnt <= 86.99):
        print("Final Letter Grade: B")
        print("Congratulations on Good Mastery!")
    #If the user scores between 80% and 82.99%, print B-
    elif (total_pcnt >= 80) & (total_pcnt <= 82.99):
        print("Final Letter Grade: B-")
    #If the user scores between 77% and 79.99%, print C+
    elif (total_pcnt >= 77) & (total_pcnt <= 79.99):
        print("Final Letter Grade: C+")
    #If the user scores between 73% and 77.99%, print C & a message
    elif (total_pcnt >= 73) & (total_pcnt <= 77.99):
        print("Final Letter Grade: C")
        print("Your performance is satisfactory")
    #If the user scores between 70% and 72.99%, print C-
    elif (total_pcnt >= 70) & (total_pcnt <= 72.99):
        print("Final Letter Grade: C-")
    #If the user scores between 67% and 69.99%, print D+
    elif (total_pcnt >= 67) & (total_pcnt <= 69.99):
        print("Final Letter Grade: D+")
    #If the user scores between 60% and 66.99%, print D & a message
    elif (total_pcnt >= 60) & (total_pcnt <= 66.99):
        print("Final Letter Grade: D")
        print("Unfortunately, your performance is less-than-satisfactory")
    #If the user scores under 60%, print F & a message
    elif total_pcnt <60:
        print("Final Letter Grade: F")
        print("Unfortunately, your performance is not satisfactory")
        print("You will need to retake this course")
#
############################
# Calculating Weights  #
############################
#This function calculates the weight of each assignment.
#It is called in the mainframe.
def Weight_Calc(points, weight):
    """Calculate the weights for each Assignment.

    Keyword arguments:
    points -- the number of points scored for each assignment
    weight -- the number of points that the assingment is worth out of 100
    """
    try:
        points = float(points)
        try:
            weight = float(weight)
            if (100 >= points >= 0):
                if (100 > weight > 0):
                    wt = (points/100)*weight
                else:
                    raise ValueError('Weight argument must be less than 100 and greater than 0.')
            else:
                raise ValueError('Points argument must be less than or equal to 100 and greater than or equal to 0.')
        except:
            raise TypeError('Input must be a float or integer')
    except:
            raise TypeError('Input must be a float or integer')
    return wt

#
###################
#      Main       #
###################
if __name__ == '__main__':
    # --help command line description
    parser = argparse.ArgumentParser(
    description = "This script will calculate your final grade based on the percentage grades that you input for each assignment.")
    args = parser.parse_args()
    ################################
    # Calculating Percentage Grade #
    ################################
    #This program will calculate your Semester grade based on entering percentages from each assingment
    #
    #Create a list to store each grade
    grades = []
    #
    #Before each section a line will print distinguishing which section of
    #the grade is being taken as an input
    #
    #Print section one
    print('Section 1: Discussion Grade')
    #
    #The user is prompted to enter their discussion grade
    #The script casts it as an int and assigns the integer to variable "discuss"
    discuss = input("Enter percentage grade for your Discussion Meetings: ")
    #discussion grade percentage is changed to point value
    discuss = Weight_Calc(discuss, 24)
    #discussion grade is appended to the grade list
    grades.append(discuss)
    #
    #
    #Print Section two
    print('Section 2: Assignments')
    #
    #The user is prompted to enter their About the coder assignment grade
    #The script casts it as an int and assigns the integer to variable "atc"
    atc = input("Enter percentage grade for the About the Coder assingment: ")
    #The about the coder grade percentage is changed to point value
    atc = Weight_Calc(atc, 5)
     #The about the coder grade is appended to the grade list
    grades.append(atc)
    #
    #The user is prompted to enter their Utility Script assignment grade
    #The script casts it as an int and assigns the integer to variable "us"
    us = input("Enter percentage grade for the Utility Script assingment: ")
    #The utlity script grade percentage is changed to point value
    us = Weight_Calc(us, 5)
    #The utility script grade is appended to the grade list
    grades.append(us)
    #
    #The user is prompted to enter their Sparse Data Challenge Assignment grade
    #The script casts it as an int and assigns the integer to variable "sdc"
    sdc = input("Enter percentage grade for the Sparse Data Challenge assingment: ")
    #The sparse data challenge grade percentage is changed to point value
    sdc = Weight_Calc(sdc, 5)
    #The sparse data challenge grade is appended to the grade list
    grades.append(sdc)
    #
    #The user is prompted to enter their Conversion Scripts Assignment grade
    #The script casts it as an int and assigns the integer to variable "cs"
    cs = input("Enter percentage grade for The Conversion Scripts assingment: ")
    #The conversion scripts grade percentage is changed to point value
    cs = Weight_Calc(cs, 10)
    #The conversion scripts grade is appended to the grade list
    grades.append(cs)
    #
    #The user is prompted to enter their The PEP8 Assignment grade
    #The script casts it as an int and assigns the integer to variable "pep8"
    pep8 = input("Enter percentage grade for The PEP8 assingment: ")
    #The PEP8 grade percentage is changed to point value
    pep8 = Weight_Calc(pep8, 5)
    #The PEP8 grade is appended to the grade list
    grades.append(pep8)
    #
    #
    #Print Section three
    #The user is prompted to enter their reports grade
    #The script casts it as an int and assigns the integer to variable "reports"
    print('Section 3: Reports')
    reports = input("Enter percentage grade for your reports: ")
    #The reports grade percentage is changed to point value
    reports = Weight_Calc(reports, 24)
    #The reports grade is appended to the grade list
    grades.append(reports)
    #
    #
    #Print Section four
    print('Section 4: Project')
    #The user is prompted to enter their project grade
    #The script casts it as an int and assigns the integer to variable "proj"
    proj = input("Enter percentage grade for your project: ")
    #The project grade percentage is changed to point value
    proj = Weight_Calc(proj, 22)
    #The project grade is appended to the grade list
    grades.append(proj)
    #print(grades) #uncomment to check that program correctly
    #appended grades to grade list
    #
    #Calculate the sum of points for each assignment, since the point totals add up to 100,
    #there is no need to divide by a total
    total_pcnt = sum(grades)
    #Print final perentage grade
    print("Final Grade (in percentage points):",total_pcnt,"%")
    #
    ################################
    # Print Letter Grade #
    ################################
    LetterGrade(total_pcnt)
