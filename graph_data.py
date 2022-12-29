"""CSC110 Fall 2021 Final Project: Graph Data
December 13, 2021
Cole Wiltse

This module contains a function for graphing transit data and unemployment data.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def graph_data(data: tuple[list, list, list]) -> None:
    """Use data to plot a graph with the primary y axis representing the transit data and the
    secondary y axis representing the unemployment data. The x axis will represent the dates they
    correspond to.

    Preconditions:
      - len(data) == 3
      - data[0] contains the transit data
      - data[1] contains the unemployment data
      - data[2] contains the dates for the transit and unemployment data
      - len(data[0]) > 0
      - len(data[0]) == len(data[1]) == len(data[2])
      """

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=data[2], y=data[0], name="Transit Data"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=data[2], y=data[1], name="Unemployment Data"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Transit Data versus Unemployment Data Before and After Covid"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")

    # Set y-axes titles
    fig.update_yaxes(title_text="Transit Ridership (Millions)", secondary_y=False)
    fig.update_yaxes(title_text="Unemployment Rate (Percentage)", secondary_y=True)

    fig.show()


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = True
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'allowed-io': ['load_data'],
        'extra-imports': ['python_ta.contracts', 'plotly.graph_objects', 'plotly.subplots'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        'disable': ['R1705', 'C0200'],
    })
