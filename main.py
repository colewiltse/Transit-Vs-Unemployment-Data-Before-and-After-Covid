"""CSC110 Fall 2021 Final Project: Main
December 13, 2021
Cole Wiltse


This file allows the user to choose filters for the transit datasets and unemployment datasets. It
then plots the filtered data based on the user's decisions on a graph."""
from graph_data import graph_data
from load_data import load_transit_data, load_unemployment_data
from project_system import Filters, filter_data


if __name__ == '__main__':

    run = True

    transit_data = load_transit_data('data/transit_data.csv')

    unemployment_data = load_unemployment_data('data/unemployment_data.csv')

    print("This program visualizes transit data vs unemployment data before and after covid.")

    while run:
        print("First, type in a start date in the format year-date (example, 2020-01).")
        print("Make sure the date is within the range 2017-01 to 2021-07 inclusive.")

        start_date = input('Type here: ')

        start_date_to_list = str.split(start_date, '-')
        start_year = int(start_date_to_list[0])
        start_month = int(start_date_to_list[1])

        # Check if the inputted date is in the specified range
        while not ((2017 <= start_year < 2021 and 1 <= start_month <= 12)
                   or (start_year == 2021 and 1 <= start_month <= 7)):
            print('Sorry, that was an invalid date, please try again.')
            start_date = input('Type here: ')
            start_date_to_list = str.split(start_date, '-')
            start_year = int(start_date_to_list[0])
            start_month = int(start_date_to_list[1])

        print("Next, type in an end date in the format year-date (example, 2020-01).")
        print("Make sure the date is within the range 2017-02 to 2021-08 inclusive.")
        print("Also make sure this date is greater than your start date.")

        end_date = input('Type here: ')

        end_date_to_list = str.split(end_date, '-')
        end_year = int(end_date_to_list[0])
        end_month = int(end_date_to_list[1])

        # Check if the inputted date is in the specified range and that the end date is greater than
        # the end date.
        while not ((start_year <= end_year < 2021 and 1 <= end_month <= 12)
                   or (end_year == 2021 and end_month <= 8))\
                and ((start_year < end_year)
                     or (start_year == end_year and start_month < end_month)):
            print('Sorry, that was an invalid date, please try again.')
            end_date = input('Type here: ')

            end_date_to_list = str.split(end_date, '-')
            end_year = int(end_date_to_list[0])
            end_month = int(end_date_to_list[1])

        print("Next, use the menu below to select a region to look at.")
        print("Type the number corresponding to that input to select it.")
        print("Note that all of the data is for urban transit excluding "
              "Canada (Interurban and Rural)")
        print("Also note that the unemployment data does not contain data for the Territories")
        print('1 - Canada (Urban)')
        print('2 - Canada (Interurban and rural)')
        print('3 - Atlantic provinces')
        print('4 - Quebec and Ontario')
        print('5 - Prairies, British Columbia and Territories')

        region = input('Type here: ')

        # Check if the inputted number is in the specified range.
        while not 1 <= int(region) <= 5:
            print("Sorry, that was an invalid input, please try again.")
            region = input('Type here: ')

        if region == '1':
            region = 'Canada (Urban)'
        elif region == '2':
            region = 'Canada (Interurban and rural)'
        elif region == '3':
            region = 'Atlantic'
        elif region == '4':
            region = 'Quebec and Ontario'
        elif region == '5':
            region = 'Prairies, British Columbia and Territories'

        print("Next, use the menu below to select the type of unemployment to look at.")
        print("Type the number corresponding to that input to select it.")
        print('1 - unemployed 1 year or more')
        print('2 - unemployed 3 months or more')
        print('3 - comparable to the United States rate')
        print('4 - official rate')
        print('5 - plus discouraged searchers')
        print('6 - plus waiting group (recall, replies, long-term future starts)')
        print('7 - plus involuntary part-timers (in full-time equivalents)')
        print('8 - R8 - plus discouraged searchers,'
              ' waiting group, portion of involuntary part-timers')

        type_of_unemployment = input('Type here: ')

        # Check if the inputted number is in the specified range.
        while not 1 <= int(type_of_unemployment) <= 8:
            print("Sorry, that was an invalid input, please try again.")
            type_of_unemployment = input('Type here: ')

        if type_of_unemployment == '1':
            type_of_unemployment = 'R1 - unemployed 1 year or more'
        elif type_of_unemployment == '2':
            type_of_unemployment = 'R2 - unemployed 3 months or more'
        elif type_of_unemployment == '3':
            type_of_unemployment = 'R3 - comparable to the United States rate'
        elif type_of_unemployment == '4':
            type_of_unemployment = 'R4 - official rate'
        elif type_of_unemployment == '5':
            type_of_unemployment = 'R5 - plus discouraged searchers'
        elif type_of_unemployment == '6':
            type_of_unemployment = 'R6 - plus waiting group' \
                                   ' (recall, replies, long-term future starts)'
        elif type_of_unemployment == '7':
            type_of_unemployment = 'R7 - plus involuntary part-timers (in full-time equivalents)'
        elif type_of_unemployment == '8':
            type_of_unemployment = 'R8 - plus discouraged searchers,' \
                                   ' waiting group, portion of involuntary part-timers'

        print("Next, use the menu below to select the sex of the unemployment data.")
        print(" Type the number corresponding to that input to select it.")
        print('1 - Both sexes')
        print('2 - Males')
        print('3 - Females')
        sex = input('Type here: ')

        # Check if the inputted number is in the specified range.
        while not 1 <= int(sex) <= 3:
            print("Sorry, that was an invalid input, please try again.")
            sex = input('Type here: ')

        if sex == '1':
            sex = 'Both sexes'
        elif sex == '2':
            sex = 'Males'
        elif sex == '3':
            sex = 'Females'

        print("Next, use the menu below to select the age group of the unemployment data.")
        print("Type the number corresponding to that input to select it.")
        print('1 - 15 years and over')
        print('2 - 15 to 24 years')
        print('3 - 25 years and over')
        print('4 - 25 to 44 years')
        print('5 - 45 years and over')
        print('6 - 25 to 54 years')
        print('7 - 55 years and over')
        print('8 - 55 to 64 years')
        print('9 - 65 years and over')

        age = input('Type here: ')

        # Check if the inputted number is in the specified range.
        while not 1 <= int(age) <= 9:
            print("Sorry, that was an invalid input, please try again.")
            age = input('Type here: ')

        if age == '1':
            age = '15 years and over'
        elif age == '2':
            age = '15 to 24 years'
        elif age == '3':
            age = '25 years and over'
        elif age == '4':
            age = '25 to 44 years'
        elif age == '5':
            age = '45 years and over'
        elif age == '6':
            age = '25 to 54 years'
        elif age == '7':
            age = '55 years and over'
        elif age == '8':
            age = '55 to 64 years'
        elif age == '9':
            age = '65 years and over'

        filters = Filters(start_date, end_date, region, type_of_unemployment, sex, age)

        # Get the filtered data.
        data = filter_data(transit_data, unemployment_data, filters)

        # Plot the filtered data.
        graph_data(data)

        is_valid_choice = False

        print('Do you want to make another graph with different filters? Type Y or N to choose.')
        choice = input('Type here: ')
        if choice == 'Y':
            print('The process for filtering data will now begin again.')
            is_valid_choice = True
        elif choice == 'N':
            print('The program will now end. Thank you!')
            run = False
            is_valid_choice = True

        # Check if the input was valid.
        while not is_valid_choice:
            print('That was an invalid input, please try again.')
            choice = input('Type here: ')
            if choice == 'Y':
                print('The process for filtering data will now begin again.')
                is_valid_choice = True
            elif choice == 'N':
                print('The program will now end. Thank you!')
                run = False
                is_valid_choice = True
