# -*- encoding: utf-8 -*-
# This class implements plot scripts

import pandas as pd


def plot_bar(y, x) -> None:
    df = pd.DataFrame(y, index=x)
    df.plot.bar(rot=0, subplots=True)
