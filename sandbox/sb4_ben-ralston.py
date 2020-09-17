import os


def validate_raster(file):
    int_tags = ['ncols', 'nrows']
    float_tags = ['xllcorner', 'yllcorner', 'xllcenter', 'yllcenter',
                  'cellsize', 'nodata_value']
    tag_dict = {tag: None for tag in int_tags + float_tags}

    row_count = 0
    for counter, line in enumerate(file):
        split_line = line.strip().split()

        process_row = True
        if len(split_line) == 2:

            if not is_number(split_line[0]):
                if row_count:
                    return ('Tag defined after first row of data on line %d' %
                            (counter + 1))

                process_row = False
                tag = split_line[0].lower()
                valid_int_tag = tag in int_tags
                valid_float_tag = tag in float_tags

                if not (valid_int_tag or valid_float_tag):
                    return 'Invalid tag on line %d' % (counter + 1)

                if valid_int_tag:
                    if not is_int(split_line[1]):
                        return 'Incorrect value type on line %d' % (counter + 1)
                    tag_dict[tag] = int(split_line[1])

                else:
                    try:
                        value = float(split_line[1])
                    except ValueError:
                        return 'Incorrect value type on line %d' % (counter + 1)
                    tag_dict[tag] = value

        if process_row and split_line:
            return_value = validate_row(split_line, tag_dict)
            if return_value is True:
                row_count += 1
            else:
                return return_value % (counter + 1)

    valid_tags = validate_tags(tag_dict)
    if valid_tags is not True:
        return valid_tags

    if row_count != tag_dict['nrows']:
        return 'Number of rows does not match NROWS tag'

    valid_dimensions = validated_dimensions(tag_dict)
    if valid_dimensions is not True:
        return valid_dimensions

    return True


def validate_tags(tag_dict):
    required_tags = ['ncols', 'nrows', 'cellsize']
    x_coord = ['xllcenter', 'xllcorner']
    y_coord = ['yllcenter', 'yllcorner']

    for tag in required_tags:
        if tag_dict[tag] is None:
            return '%s was not defined' % tag.upper()

    x_tag_none = [tag_dict[tag] is None for tag in x_coord]
    y_tag_none = [tag_dict[tag] is None for tag in y_coord]

    if x_tag_none[0] and x_tag_none[1]:
        return 'Lower left cell X-coordinate not defined'
    elif not (x_tag_none[0] or x_tag_none[1]):
        return 'XLLCENTER and XLLCORNER both defined ' \
               '(only one should be defined)'

    if y_tag_none[0] and y_tag_none[1]:
        return 'Lower left cell Y-coordinate not defined'
    elif not (y_tag_none[0] or y_tag_none[1]):
        return 'YLLCENTER and YLLCORNER both defined ' \
               '(only one should be defined)'

    return True


def validate_row(row_list, tag_dict):

    if len(row_list) != tag_dict['ncols']:
        return 'Incorrect number of columns on line %d'

    is_number_list = [is_number(element) for element in row_list]

    # Index code found on https://stackoverflow.com/questions/6294179
    # /how-to-find-all-occurrences-of-an-element-in-a-list
    non_numeric_indices = [str(i + 1) for i, x in enumerate(is_number_list)
                           if x is False]

    if non_numeric_indices:
        if len(non_numeric_indices) == 1:
            return_string = ('Non-numeric value at position %s' %
                             non_numeric_indices[0])
            return return_string + ' on line %d'
        else:
            indices_string = '[%s]' % ','.join(non_numeric_indices)
            return_string = ('Non-numeric value at positions %s' %
                             indices_string)
            return return_string + ' on line %d'

    return True


def validated_dimensions(tag_dict):
    total_longitude = tag_dict['cellsize'] * tag_dict['ncols']
    total_latitude = tag_dict['cellsize'] * tag_dict['nrows']

    if total_longitude > 360:
        return 'Cells overlap longitudinally'
    if total_latitude > 180:
        return 'Cells overlap latitudinally'

    return True


def is_number(string):
    # Code found on https://stackoverflow.com/questions/354038
    # /how-do-i-check-if-a-string-is-a-number-float
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int(string):
    try:
        int_value = int(string)
        float_value = float(string)
    except ValueError:
        return False
    return int_value == float_value


def main():
    data_files = os.listdir('data')
    for file_name in data_files:
        extension = os.path.splitext(file_name)[1]

        if extension.lower() == '.asc':
            file_path = os.path.join('data', file_name)
            with open(file_path, 'r') as file:
                valid_raster = validate_raster(file)

            if valid_raster is True:
                print('%s is a valid raster' % file_name)
            else:
                print('%s is not a valid raster---%s' % (file_name, valid_raster))


if __name__ == '__main__':
    main()
