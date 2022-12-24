# -*- encoding: utf-8 -*-
# This class implements plot scripts
# author: steinkirch

import pandas as pd
from os import exit_with_error


def open_csv(filepath) -> dict:
    """Load and parse a csv file."""

    try:
        return pd.read_csv(filepath)
    except (IOError, FileNotFoundError, TypeError) as e:
        exit_with_error(f'Failed to parse: "{filepath}": {e}')


def save_csv(destination, data, index=False) -> None:
    """Save data from memory to a csv destination in disk."""

    try:
        data.to_csv(destination, index=index)

    except (IOError, TypeError) as e:
        log_error(f'Could not save {destination}: {e}')


def plot_bar(y, x) -> None:
    """Simplest plot for two sets."""
    df = pd.DataFrame(y, index=x)
    df.plot.bar(rot=0, subplots=True)