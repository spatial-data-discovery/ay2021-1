"""
Author: Ben Ralston
Date: 2020-11-19

Description: This script reads the four input files, ststdnsadata.xlsx,
United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv, states.csv,
and nst-est2019-alldata.csv, and converts them into two CSV files,
unemployment_by_state.csv and monthly_covid_cases_by_state.csv.
"""

from datetime import date
from os import getcwd
from os.path import join

import pandas as pd
import numpy as np


def unemployment():
    base_df = unemployment_read_excel()
    cleaned_df = unemployment_reformat_data(base_df)

    output_name = 'unemployment_by_state.csv'
    output_path = join('IntermediateOutput', output_name)
    output_directory = join(getcwd(), 'IntermediateOutput')
    cleaned_df.to_csv(output_path, index_label='fips')

    print('Created %s in the following directory:\n%s\n' % (output_name, output_directory))


def unemployment_read_excel():
    filename = 'ststdnsadata.xlsx'
    file_path = join('Data', filename)
    col_names = ['FIPS Code', 'State', 'Year', 'Month', 'Civilian Population',
                 'Civilian Labor Force', 'Percent of Population',
                 'Total Employment', 'Percent Employment', 'Total Unemployment',
                 'Percent Unemployment']

    raw_df = pd.read_excel(file_path, names=col_names)

    rows_to_drop = [i for i in range(7)]
    raw_df.drop(labels=rows_to_drop, inplace=True)

    raw_df['Year'] = raw_df['Year'].astype(np.int32)
    raw_df['Month'] = raw_df['Month'].astype(np.int32)

    return raw_df


def unemployment_reformat_data(raw_df):
    states = ['Alabama',
              'Alaska',
              'Arizona',
              'Arkansas',
              'California',
              'Colorado',
              'Connecticut',
              'Delaware',
              'District of Columbia',
              'Florida',
              'Georgia',
              'Hawaii',
              'Idaho',
              'Illinois',
              'Indiana',
              'Iowa',
              'Kansas',
              'Kentucky',
              'Louisiana',
              'Maine',
              'Maryland',
              'Massachusetts',
              'Michigan',
              'Minnesota',
              'Mississippi',
              'Missouri',
              'Montana',
              'Nebraska',
              'Nevada',
              'New Hampshire',
              'New Jersey',
              'New Mexico',
              'New York',
              'North Carolina',
              'North Dakota',
              'Ohio',
              'Oklahoma',
              'Oregon',
              'Pennsylvania',
              'Rhode Island',
              'South Carolina',
              'South Dakota',
              'Tennessee',
              'Texas',
              'Utah',
              'Vermont',
              'Virginia',
              'Washington',
              'West Virginia',
              'Wisconsin',
              'Wyoming']
    fips_codes = []

    for row in raw_df.iterrows():
        if row[1]['State'] in states:
            fips_codes.append(row[1]['FIPS Code'])

        if len(fips_codes) == len(states):
            break

    cleaned_df = pd.DataFrame(data={}, columns=fips_codes)

    null_row = {code: None for code in fips_codes}
    process_counter = 0

    print('Started processing ststdnsadata.xlsx')

    for row in raw_df.iterrows():
        process_counter += 1
        if process_counter % 1000 == 0:
            print('Processing row %d' % process_counter)

        if row[1]['State'] not in states:
            continue

        current_date = date(row[1]['Year'], row[1]['Month'], 1)

        if current_date not in cleaned_df.index:
            null_df = pd.DataFrame(null_row, columns=fips_codes,
                                   index=[current_date])
            cleaned_df = cleaned_df.append(null_df)

        cleaned_df.loc[current_date, row[1]['FIPS Code']] = row[1]['Percent Unemployment']

    print('Finished processing ststdnsadata.xlsx\n')

    return cleaned_df.transpose()


def covid():
    base_df = covid_read_csv()
    monthly_cases_df = covid_reformat_data(base_df)
    state_pop_df = read_state_population_csv()
    state_centers_df = read_state_centers_csv()

    merged = pd.merge(state_centers_df, monthly_cases_df, how='inner', left_on='State',
                      right_index=True)

    for state in merged['State Long']:
        population = state_pop_df.loc[state_pop_df['State'] == state, 'Population'].to_numpy()[0]
        row = merged['State Long'] == state
        for i in range(1, 12):
            current_date = date(2020, i, 1)
            merged.loc[row, current_date] *= 100000 / population

    output_name = 'monthly_covid_cases_by_state.csv'
    output_path = join('IntermediateOutput', output_name)
    output_directory = join(getcwd(), 'IntermediateOutput')
    merged.to_csv(output_path, index=False)

    print('Created %s in the following directory:\n%s' % (output_name, output_directory))


def covid_read_csv():
    filename = 'United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv'
    file_path = join('Data', filename)
    raw_df = pd.read_csv(file_path)

    raw_df['submission_date'] = pd.to_datetime(raw_df['submission_date'])

    trimmed_df = pd.DataFrame({'Date': raw_df['submission_date'],
                               'State Abbr': raw_df['state'],
                               'New Cases': raw_df['new_case']})
    return trimmed_df


def covid_reformat_data(raw_df):
    column_names = []
    for i in range(1, 12):
        column_names.append(date(2020, i, 1))

    cases_by_month = pd.DataFrame({}, columns=column_names)

    null_row = {column: None for column in column_names}

    process_counter = 0
    running_count = 0
    current_month = None
    current_state = None

    print('Started processing United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv')

    for row in raw_df.iterrows():
        process_counter += 1
        if process_counter % 1000 == 0:
            print('Processing row %d' % process_counter)

        if row[1]['State Abbr'] not in cases_by_month.index:
            if current_state:
                prev_date = date(2020, current_month, 1)
                cases_by_month.loc[current_state, prev_date] = running_count

            current_month = None
            current_state = row[1]['State Abbr']
            null_df = pd.DataFrame(null_row, columns=column_names,
                                   index=[row[1]['State Abbr']])
            cases_by_month = cases_by_month.append(null_df)

        if current_month != row[1]['Date'].month:
            if current_month is not None:
                prev_date = date(2020, current_month, 1)
                cases_by_month.loc[current_state, prev_date] = running_count

            current_month = row[1]['Date'].month
            running_count = row[1]['New Cases']

        else:
            running_count += row[1]['New Cases']

    # Insert final value into dataframe:
    prev_date = date(2020, current_month, 1)
    cases_by_month.loc[current_state, prev_date] = running_count

    print('Finished processing United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv\n')

    return cases_by_month


def read_state_population_csv():
    filename = 'nst-est2019-alldata.csv'
    file_path = join('Data', filename)
    raw_df = pd.read_csv(file_path)

    trimmed_df = pd.DataFrame({'State': raw_df['NAME'],
                               'Population': raw_df['POPESTIMATE2019']})
    return trimmed_df


def read_state_centers_csv():
    filename = 'states.csv'
    file_path = join('Data', filename)
    raw_df = pd.read_csv(file_path)

    # Only looking at states so we remove Puerto Rico:
    pr_ind = list(raw_df['state'] == 'PR').index(True)
    raw_df.drop(index=pr_ind, inplace=True)

    trimmed_df = pd.DataFrame({'lon': raw_df['longitude'],
                               'lat': raw_df['latitude'],
                               'State': raw_df['state'],
                               'State Long': raw_df['name']})
    return trimmed_df


def main():
    unemployment()
    covid()


if __name__ == '__main__':
    main()
