"""CSC110 Fall 2021 Final Project: Project System
December 13, 2021
Cole Wiltse


This module contains datasets for the transit data, unemployment data, and filters. This module
also contains a function which filters the datasets and returns the values required for plotting
the data on a graph."""


from dataclasses import dataclass

TRANSIT_REGIONS = {'Canada (Urban)',
                   'Canada (Interurban and rural)',
                   'Atlantic',
                   'Quebec and Ontario',
                   'Prairies, British Columbia and Territories'}

UNEMPLOYMENT_REGIONS = {'Canada',
                        'Atlantic',
                        'Quebec and Ontario',
                        'Prairies, British Columbia and Territories'}

UNEMPLOYMENT_TYPES = {'R1 - unemployed 1 year or more',
                      'R2 - unemployed 3 months or more',
                      'R3 - comparable to the United States rate',
                      'R4 - official rate',
                      'R5 - plus discouraged searchers',
                      'R6 - plus waiting group (recall, replies, long-term future starts)',
                      'R7 - plus involuntary part-timers (in full-time equivalents)',
                      'R8 - plus discouraged searchers,'
                      ' waiting group, portion of involuntary part-timers'}

SEXES = {'Both sexes', 'Males', 'Females'}

AGES = {'15 years and over',
        '15 to 24 years',
        '25 years and over',
        '25 to 44 years',
        '45 years and over',
        '25 to 54 years',
        '55 years and over',
        '55 to 64 years',
        '65 years and over'}


@dataclass
class Filters:
    """A data class representing filters for the transit and unemployment data.

    Instance Attributes:
      - start_date: the start date for the data
      - end_date: the end date for the data
      - region: the region for the data
      - type_of_unemployment: the specific type of unemployment for the Unemployment data
      - sex: the sex of the Unemployment data
      - age: the age range of the Unemployment data

    Representation Invariants:
      - self.start_date and self.end_date are in the format year-date (example: 2020-01)
      - self.start_date is in the range 2017-01 to 2021-07 inclusive
      - self.end_date is in the range 2017-02 to 2021-08 inclusive
      - self.start_date is greater than self.end_date
      - self.region in TRANSIT_REGIONS
      - self.type_of_unemployment in UNEMPLOYMENT_TYPES
      - self.sex in SEXES
      - self.age in AGES
    """
    start_date: str
    end_date: str
    region: str
    type_of_unemployment: str
    sex: str
    age: str


@dataclass
class TransitData:
    """A data class representing an instance of transit data.

    Instance Attributes:
      - date: the date of the data
      - region: the region of the data
      - value: the volume of transit data in the millions for the data
      - is_valid: says whether this data is considered valid

    Representation Invariants:
      - date is in the format year-date (example: 2020-01)
      - self.region in TRANSIT_REGIONS
      - self.value >= 0
    """
    date: str
    region: str
    value: float
    is_valid: bool


@dataclass
class UnemploymentData:
    """A data class representing an instance of Unemployment data.

    Instance Attributes:
      - start_date: the start date for the data
      - end_date: the end date for the data
      - region: the region for the data
      - type_of_unemployment: the specific type of unemployment for the Unemployment data
      - sex: the sex of the Unemployment data
      - age: the age range of the Unemployment data

    Representation Invariants:
      - date is in the format year-date (example: 2020-01)
      - self.region in UNEMPLOYMENT_REGIONS
      - self.type_of_unemployment in UNEMPLOYMENT TYPES
      - self.sex in SEXES
      - self.age in AGES
      - self.value >= 0
    """
    date: str
    region: str
    unemployment_type: str
    sex: str
    age: str
    value: float
    is_valid: bool


def filter_data(transit_data: list[TransitData], unemployment_data: list[UnemploymentData],
                filters: Filters) -> tuple[list, list, list]:
    """Filters the data from transit_data and unemployment_data based on filters and return a tuple
    containing the values from transit_data, unemployment_data, and their corresponding dates in
    that order. (Note when referring to transit_data and unemployment_data, I am referring to the
    arguments of this function, not the datasets transit_data and unemployment_data.)

    Preconditions:
      - len(transit_data) > 0
      - len(unemployment_data) > 0
    """
    # ACCUMULATOR transit_data_so_far: Keep track of the filtered transit data seen so far in the
    # first loop.
    transit_data_so_far = []

    # ACCUMULATOR unemployment_data_so_far: Keep track of the filtered unemployment data seen so far
    # in the first loop.
    unemployment_data_so_far = []

    # ACCUMULATOR transit_values_so_far: Keep track of the transit ridership values seen so far in
    # the second loop.
    transit_values_so_far = []

    # ACCUMULATOR unemployment_values_so_far: Keep track of the unemployment percentage values seen
    # so far in the second loop.
    unemployment_values_so_far = []

    # ACCUMULATOR dates_so_far: Keep track of the dates of the values seen so far in the second
    # loop.
    dates_so_far = []

    start_date_to_list = str.split(filters.start_date, '-')
    start_year = int(start_date_to_list[0])
    start_month = int(start_date_to_list[1])

    end_date_to_list = str.split(filters.end_date, '-')
    end_year = int(end_date_to_list[0])
    end_month = int(end_date_to_list[1])

    for row in transit_data:
        current_date_to_list = str.split(row.date, '-')
        current_year = int(current_date_to_list[0])
        current_month = int(current_date_to_list[1])

        # Check if the date of the current TransitData is in the specified range.
        if start_year < current_year < end_year or \
                (start_year == current_year and start_month <= current_month) or\
                (current_year == end_year and current_month <= end_month):
            if row.region == filters.region:
                transit_data_so_far.append(row)

    # Here I change the region to Canada so that it can work with UnemploymentData.
    if filters.region == "Canada (Urban)" or filters.region == "Canada (Interurban and rural)":
        filters.region = "Canada"

    for row in unemployment_data:
        current_date_to_list = str.split(row.date, '-')
        current_year = int(current_date_to_list[0])
        current_month = int(current_date_to_list[1])

        # Check if the date is in the specified range.
        if start_year < current_year < end_year or \
                (start_year == current_year and start_month <= current_month) or \
                (current_year == end_year and current_month <= end_month):

            # Use filters to check if the current instance of Unemployment Data is what was
            #  specified.
            if row.region == filters.region\
                    and row.unemployment_type == filters.type_of_unemployment\
                    and row.sex == filters.sex\
                    and row.age == filters.age:
                unemployment_data_so_far.append(row)

    # Check both the current TransitData and UnemploymentData to make sure both are valid
    for i in range(len(transit_data_so_far)):
        if transit_data_so_far[i].is_valid and unemployment_data_so_far[i].is_valid:
            transit_values_so_far.append(transit_data_so_far[i].value)
            unemployment_values_so_far.append(unemployment_data_so_far[i].value)
            dates_so_far.append(unemployment_data_so_far[i].date)

    return (transit_values_so_far, unemployment_values_so_far, dates_so_far)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = True
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv', 'load_data'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        'disable': ['R1705', 'C0200'],
    })
