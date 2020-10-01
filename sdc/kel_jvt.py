import os

def isFloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def checkRaster(red_path, blue_path, green_path, final_path):
    totalrows = 0

    red = open(red_path, "r")
    blue = open(blue_path, "r")
    green = open(green_path, "r")
    final = open(final_path, "w+")

    for red_line, blue_line, green_line in zip(red, blue, green):
        if totalrows >= 0 and totalrows <= 6:
            totalrows += 1
            final.write(red_line)
        else:
            red_row_values = red_line.split()
            blue_row_values = blue_line.split()
            green_row_values = green_line.split()
            final_row_values = []
            if len(red_row_values) != len(blue_row_values) or len(green_row_values) != len(blue_row_values):
                print("Error, line "+str(totalrows)+" does not contain the number of cols defined in the header.")
                return
            for i in range(len(red_row_values)):
                if red_row_values[i] == "-9999":
                    red_row_values[i] = "0"
                if blue_row_values[i] == "-9999":
                    blue_row_values[i] = "0"
                if green_row_values[i] == "-9999":
                    green_row_values[i] = "0"
                
                final_row_values.append(str(int(red_row_values[i])+int(blue_row_values[i])+int(green_row_values[i])))

            sum_row_values = ""
            if len(final_row_values) != len(red_row_values):
                print("ERROR: The number of columns in finals rows does not match that of the original files")
                return
            for i in range(len(final_row_values)-1):
                sum_row_values = sum_row_values + final_row_values[i] + " "
            sum_row_values = sum_row_values + final_row_values[-1] + "\n"
            final.write(sum_row_values)
            totalrows += 1
    red.close()
    blue.close()
    green.close()
    final.close()


if __name__ == "__main__":
    red_path = ""
    blue_path = ""
    green_path = ""
    final_path = ""
    path = os.getcwd()
    if '/' in path:
        red_path = path + '/red.asc'
        blue_path = path + '/blue.asc'
        green_path = path + '/green.asc'
        final_path = path + '/kel_jvt.asc'
    else:
        red_path = path + r'\red.asc'
        blue_path = path + r'\blue.asc'
        green_path = path + r'\green.asc'
        final_path = path + r'\kel_jvt.asc'

    if os.path.isfile(red_path) and os.path.isfile(blue_path) and os.path.isfile(green_path):
        checkRaster(red_path, blue_path, green_path, final_path)
    else:
        print("At least one of the files is not valid.")