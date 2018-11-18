"""This module handles heatmaps."""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class HeatMap(object):
    """Creates HeatMaps from data."""

    def __init__(self, csv_path):
        self.df = self._load_data(csv_path)

    def _load_data(self, csv_path):
        """Parse data to create an usable dataframe."""
        df = pd.read_csv(csv_path)
        df = df.set_index("date")
        df = pd.pivot_table(df, columns=df["activity"], index=df.index, aggfunc=sum).fillna(0)

        # add missing dates
        df.index = pd.to_datetime(df.index)
        idx = pd.date_range(df.index.min(), df.index.max())
        df = df.reindex(idx, fill_value=0)[::-1]  # from older to newer
        return df

    @staticmethod
    def _create_heatmap(df):
        """Creates a HeatMap given a dataframe."""
        activity_list = df.columns.levels[1]
        dates = df.index.strftime("%Y-%m-%d")
        plt.figure(figsize=(len(activity_list) * 0.5, len(dates) * 0.35))
        plt.pcolor(df, cmap="Purples", edgecolor='k')
        plt.colorbar()
        plt.yticks(np.arange(0.5, len(dates), 1), dates)
        plt.xticks(np.arange(0.5, len(activity_list), 1), activity_list, rotation=90)
        plt.tick_params(axis="x", top=True, labelbottom=True, labeltop=True, which="both")
        plt.show()

    def _resample(self, rule):
        """Resamples dataframe."""
        df = self.df.resample(rule).sum()
        df.index = df.index[::-1]
        return df

    def create_dayly(self):
        """Creates a HeatMap with dayly data."""
        self._create_heatmap(self.df)

    def create_weekly(self):
        """Creates a HeatMap with weekly data."""
        df = self._resample('W')
        self._create_heatmap(df)

    def create_monthly(self):
        """Creates a HeatMap with monthly data."""
        df = self._resample('M')
        self._create_heatmap(df)

    def create_yearly(self):
        """Creates a HeatMap with yearly data."""
        df = self._resample('Y')
        self._create_heatmap(df)
