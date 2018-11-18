import matplotlib.pyplot as plt
import pandas as pd


class TotalHoursBar(object):
    """Creates HeatMaps from data."""

    def __init__(self, csv_path):
        self.df = self._load_data(csv_path)

    def _load_data(self, csv_path):
        """Parse data to create an usable dataframe."""
        df = pd.read_csv(csv_path)
        df = df[["activity", "time"]]
        df = df.pivot_table(index=df.activity, aggfunc=sum).fillna(0)
        return df

    def create(self):
        """Creates a bar plot using the loaded DataFrame."""
        ax = self.df.plot(kind="bar", color='b')
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.show()
