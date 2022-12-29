"""CSC110 Fall 2021 Final Project: Load Data
December 13, 2021
Cole Wiltse

This module loads the data from the transit and unemployment datasets
and filter/aggregates the necessary data.
"""
import csv
from project_system import TransitData, UnemploymentData


def load_transit_data(filename: str) -> list[TransitData]:
    """Load the data from the transit data and return a list of TransitData.

    The data in filename is in a csv format with 15 columns. The first column is the date, the
    second column is the region, the third specifies whether the data for that region is urban only
    or interurban and rural, the twelfth column is the total number of people who took public
    transit in the millions, and the thirteenth column specifies whether this row of data is valid.
    If the row of data is invalid, the value is an empty string.


    Preconditions:
      - The file used is in the specified format from Statistics Canada for public transit data.
    """
    # ACCUMULATOR: data_so_far: Keep track of the appropriate rows of data seen so far in the loop.
    data_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:

            # This is so the value can be considered a float when used as an argument in an instance
            # of TransitData
            if row[12] == "..":
                row[11] = str(0)

            # Here I check the values of the rows to make sure it should be added to data_so_far
            if row[4] == "Total passenger trips" and row[1] == "Canada" and\
                    row[3] == "Urban transit systems [485110]":
                data_so_far.append(TransitData(row[0], row[1] + " (Urban)",
                                               float(row[11]), row[12] != ".."))
            elif row[4] == "Total passenger trips" and row[1] == "Canada" and\
                    row[3] == "Interurban and rural bus transportation [485210]":
                data_so_far.append(TransitData(row[0], row[1] + " (Interurban and rural)",
                                               float(row[11]), row[12] != ".."))
            elif row[4] == "Total passenger trips":
                data_so_far.append(TransitData(row[0], row[1], float(row[11]), row[12] != ".."))

    return data_so_far


def load_unemployment_data(filename: str) -> list[UnemploymentData]:
    """Load the data from the unemployment data and return a list of UnemploymentData.

    The data in filename is in a csv format with 17 columns. The first is the date, the second is
    the region, the fourth specifies the type of unemployment, the fifth specifies the sex of the
    people in the data, the sixth specifies the age of the people in the data, the thirteenth is the
    percentage of people unemployed, and the fourteenth says if the data for that date is a valid
    set of data. If it is an invalid row of data, the value is simply an empty string.

    Preconditions:
      - The file used is in the specified format from Statistics Canada for unemployment data.
    """
    start_year, start_month, end_year, end_month = 2017, 1, 2021, 8

    # ACCUMULATOR (region)_so_far: Keep track of the data for (region) seen so far in the
    # first loop.
    canada_data_so_far, \
        nf_and_labrador_data_so_far, \
        pei_data_so_far, \
        nova_scotia_data_so_far, \
        new_brunswick_data_so_far, \
        quebec_data_so_far, \
        ontario_data_so_far, \
        manitoba_data_so_far, \
        saskatchewan_data_so_far, \
        alberta_data_so_far, \
        british_columbia_data_so_far = [], [], [], [], [], [], [], [], [], [], []

    # ACCUMULATOR data_so_far: Keep track of the final data to return seen so far in the
    # second loop.
    data_so_far = []

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:

            # This is so the value can be used when calculating the average of the data for its
            # region later, even if it is invalid.
            if row[12] == "":
                row[12] = str(0)

            date_to_list = str.split(row[0], '-')
            current_year = int(date_to_list[0])
            current_month = int(date_to_list[1])

            # Here I check if the date is within the proper range.
            if (start_year < current_year < end_year) or\
                    (start_year == current_year and start_month <= current_month) or \
                    (current_year == end_year and current_month <= end_month):

                # Here I sort the the current row by its location.
                sort_data1(row,
                           canada_data_so_far,
                           nf_and_labrador_data_so_far,
                           pei_data_so_far,
                           nova_scotia_data_so_far)

                sort_data2(row,
                           new_brunswick_data_so_far,
                           quebec_data_so_far,
                           ontario_data_so_far,
                           manitoba_data_so_far)

                sort_data3(row,
                           saskatchewan_data_so_far,
                           alberta_data_so_far,
                           british_columbia_data_so_far)

    # Here I aggregate the data by their location so that it follows the same format seen in
    # the transit data.
    for i in range(len(canada_data_so_far)):
        data_so_far.append(UnemploymentData(canada_data_so_far[i][0],
                                            'Canada',
                                            canada_data_so_far[i][2],
                                            canada_data_so_far[i][3],
                                            canada_data_so_far[i][4],
                                            float(canada_data_so_far[i][5]),
                                            canada_data_so_far[i][6]))

        current_row = UnemploymentData(nf_and_labrador_data_so_far[i][0],
                                       "Atlantic",
                                       nf_and_labrador_data_so_far[i][2],
                                       nf_and_labrador_data_so_far[i][3],
                                       nf_and_labrador_data_so_far[i][4],
                                       (float(nf_and_labrador_data_so_far[i][5])
                                        + float(pei_data_so_far[i][5])
                                        + float(nova_scotia_data_so_far[i][5])
                                        + float(new_brunswick_data_so_far[i][5])) / 4,
                                       all([nf_and_labrador_data_so_far[i][6],
                                            pei_data_so_far[i][6],
                                            nova_scotia_data_so_far[i][6],
                                            new_brunswick_data_so_far[i][6]]))
        data_so_far.append(current_row)

        current_row = UnemploymentData(quebec_data_so_far[i][0],
                                       "Quebec and Ontario",
                                       quebec_data_so_far[i][2],
                                       quebec_data_so_far[i][3],
                                       quebec_data_so_far[i][4],
                                       (float(quebec_data_so_far[i][5])
                                        + float(ontario_data_so_far[i][5]) / 2),
                                       all([quebec_data_so_far[i][6],
                                            ontario_data_so_far[i][6]]))
        data_so_far.append(current_row)

        current_row = UnemploymentData(manitoba_data_so_far[i][0],
                                       "Prairies, British Columbia and Territories",
                                       manitoba_data_so_far[i][2],
                                       manitoba_data_so_far[i][3],
                                       manitoba_data_so_far[i][4],
                                       (float(manitoba_data_so_far[i][5])
                                        + float(saskatchewan_data_so_far[i][5])
                                        + float(alberta_data_so_far[i][5])
                                        + float(british_columbia_data_so_far[i][5]))
                                       / 4,
                                       all([manitoba_data_so_far[i][6],
                                            saskatchewan_data_so_far[i][6],
                                            alberta_data_so_far[i][6],
                                            british_columbia_data_so_far[i][6]]))
        data_so_far.append(current_row)

    return data_so_far


def sort_data1(row: list,
               canada_data_so_far: list,
               nf_and_labrador_data_so_far: list,
               pei_data_so_far: list,
               nova_scotia_data_so_far: list) -> None:
    """Sort row by its location by appending its essential values to the appropriate
     list if its location matches. These essential values include its date, location, type of
     unemployment, sex, age, percentage value, and whether it is valid.

     This specific function checks if row's location is Canada, Newfoundland and Labrador, Prince
     Edward Island, or Nova Scotia.

    Preconditions
      - row is in the format specified in load_unemployment_data
    """
    if row[1] == "Canada":
        canada_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Newfoundland and Labrador":
        nf_and_labrador_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Prince Edward Island":
        pei_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Nova Scotia":
        nova_scotia_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])


def sort_data2(row: list,
               new_brunswick_data_so_far: list,
               quebec_data_so_far: list,
               ontario_data_so_far: list,
               manitoba_data_so_far: list,
               ) -> None:
    """Sort row by its location by appending its essential values to the appropriate
     list if its location matches. These essential values include its date, location, type of
     unemployment, sex, age, percentage value, and whether it is valid.

     This specific function check if row's location is New Brunswick, Quebec, Ontario, or Manitoba.

    Preconditions
      - row is in the format specified in load_unemployment_data
    """
    if row[1] == "New Brunswick":
        new_brunswick_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Quebec":
        quebec_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Ontario":
        ontario_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Manitoba":
        manitoba_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])


def sort_data3(row: list,
               saskatchewan_data_so_far: list,
               alberta_data_so_far: list,
               british_columbia_data_so_far: list) -> None:
    """Sort row by its location by appending its essential values to the appropriate
     list if its location matches. These essential values include its date, location, type of
     unemployment, sex, age, percentage value, and whether it is valid.

     This specific function check's if row's location is Saskatchewan, Alberta, or British Columbia.

    Preconditions
      - row is in the format specified in load_unemployment_data
    """
    if row[1] == "Saskatchewan":
        saskatchewan_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "Alberta":
        alberta_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])
    elif row[1] == "British Columbia":
        british_columbia_data_so_far.append([
            row[0], row[1], row[3], row[4], row[5], row[12], row[13] != "x"])


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'allowed-io': ['load_transit_data', 'load_unemployment_data'],
        'extra-imports': ['python_ta.contracts', 'csv', 'project_system'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        'disable': ['R1705', 'C0200'],
    })
