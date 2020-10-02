import csv

try:
    import numpy as np
    imported_np = True
except ImportError:
    imported_np = False

try:
    from PIL import Image
    imported_pil = True
except ImportError:
    imported_pil = False


def read_raster(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    headers = ''
    matrix = []
    for i, line in enumerate(lines):
        if i < 7:
            headers += line.strip() + '\n'
            continue

        split_line = line.strip().split()
        split_line = list(map(int, split_line))
        matrix.append(split_line)

    return matrix, headers


def write_raster(filename, matrix, headers):
    with open(filename, 'w+') as file:
        file.write(headers)

        writer = csv.writer(file, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        for line in matrix:
            writer.writerow(line)


def fix_raster(matrix):
    width = len(matrix[0])
    height = len(matrix)

    copied_matrix = []

    for row in matrix:
        copied_matrix.append(row[:])

    for i in range(height):
        for j in range(width):
            if copied_matrix[i][j] != -9999:
                continue

            distance = 1
            while True:
                nearby_cells = get_nearby_cells(width, height, i, j, distance)
                numerator = 0
                divisor = 0

                all_null = True
                for (ii, jj) in nearby_cells:
                    if matrix[ii][jj] != -9999:
                        numerator += matrix[ii][jj]
                        divisor += 1
                        all_null = False

                if not all_null:
                    average = numerator / divisor
                    copied_matrix[i][j] = int(round(average))
                    break

                distance += 1

    return copied_matrix


def get_nearby_cells(width, height, row, col, distance):
    low_col = None
    high_col = None
    low_row = None
    high_row = None

    if row - distance >= 0:
        low_row = row - distance

    if row + distance <= height - 1:
        high_row = row + distance

    if col - distance >= 0:
        low_col = col - distance

    if col + distance <= width - 1:
        high_col = col + distance

    cell_set = set()

    if low_row is not None:

        if low_col is not None and high_col is not None:
            for j in range(low_col, high_col + 1):
                cell_set.add((low_row, j))
        elif low_col is not None:
            for j in range(low_col, width):
                cell_set.add((low_row, j))
        elif high_col is not None:
            for j in range(0, high_col + 1):
                cell_set.add((low_row, j))

    if high_row is not None:

        if low_col is not None and high_col is not None:
            for j in range(low_col, high_col + 1):
                cell_set.add((high_row, j))
        elif low_col is not None:
            for j in range(low_col, width):
                cell_set.add((high_row, j))
        elif high_col is not None:
            for j in range(0, high_col + 1):
                cell_set.add((high_row, j))

    if low_col is not None:

        if low_row is not None and high_row is not None:
            for i in range(low_row + 1, high_row):
                cell_set.add((i, low_col))
        elif low_row is not None:
            for i in range(low_row + 1, height):
                cell_set.add((i, low_col))
        elif high_row is not None:
            for i in range(0, high_row):
                cell_set.add((i, low_col))

    if high_col is not None:

        if low_row is not None and high_row is not None:
            for i in range(low_row + 1, high_row):
                cell_set.add((i, high_col))
        elif low_row is not None:
            for i in range(low_row + 1, height):
                cell_set.add((i, high_col))
        elif high_row is not None:
            for i in range(0, high_row):
                cell_set.add((i, high_col))

    return cell_set


def ask_to_create_image():
    print()

    while True:
        answer = input('Would you like to create a PNG from the '
                       'corrected rasters (yes/no)? ')
        if answer.lower() in ['yes', 'no']:
            break

        print('That is not a valid response. Please enter "yes" or "no".\n')

    if answer.lower() == 'yes':
        return True
    else:
        return False


def make_png():
    file_list = ['red_bjr_cll.asc', 'green_bjr_cll.asc', 'blue_bjr_cll.asc']

    channels = []
    for file in file_list:
        matrix = read_raster(file)[0]
        np_array = np.array(matrix)
        new_image = Image.fromarray(np_array.astype('uint8'), mode='L')
        channels.append(new_image)

    image = Image.merge('RGB', (channels[0], channels[1], channels[2]))
    image.save('bjr_cll.png', 'PNG')


def main():
    file_list = ['blue.asc', 'green.asc', 'red.asc']
    add_to_name = '_bjr_cll.asc'

    for file in file_list:
        print('Processing %s.' % file)
        matrix, headers = read_raster(file)
        new_matrix = fix_raster(matrix)

        new_filename = file[:-4] + add_to_name
        write_raster(new_filename, new_matrix, headers)

    if imported_np and imported_pil:
        if ask_to_create_image():
            make_png()


if __name__ == '__main__':
    main()
