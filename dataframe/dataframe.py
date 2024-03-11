import pandas as pd
import csv
from datetime import datetime, date
import numpy as np

"""
Todo:
    - Cleanup column names
    - Remove duplicate Headers
    - Seperate Methods and Init in InselDataframes()
    - relative paths
"""


def replace_nan(val):
    return val if not np.isnan(val) else np.random.choice([1, 3])


class InselDataframes:
    def __init__(
        self,
        daily_df: pd.DataFrame = pd.DataFrame(),
        forever_df: pd.DataFrame = pd.DataFrame(),
        month_df: pd.DataFrame = pd.DataFrame(),
        forever_csv="../data/forever.csv",
        month_csv="../data",
        daily_csv="../data/daily.csv",
        reading_csv="../data/reading.csv",
    ):

        columns = [
            "Cpv",
            "Cwt",
            "Cwr",
            "Cg",
            "Cbp",
            "Cbn",
            "vw",
            "Dw",
            "Is",
            "Ta",
            "Tb",
            "Vb",
        ]
        forever_index_names = ["Date", "Type"]
        index_name = "Date"
        time_format = "%d-%m-%Y %H:%M"
        monthly_frequency = "30min"
        forever_time_format = "%d-%m-%Y"

        self.monthly_frequency = monthly_frequency
        self.forever_csv = forever_csv
        self.daily_csv = daily_csv
        self.month_csv = month_csv
        self.reading_csv = reading_csv
        self.forever_time_format = forever_time_format

        self.columns = columns
        self.time_format = time_format

        self.index_name = index_name
        self.forever_index_names = forever_index_names

        self.daily_df = daily_df
        self.month_df = month_df
        self.forever_df = forever_df

        if self.daily_df.empty:
            # Creating dummy data for daily_df
            index = pd.date_range(
                end=datetime.now().strftime(time_format),
                periods=13,
                freq="5min",
                name=index_name,
            )
            self.daily_df = pd.DataFrame(data=None, index=index, columns=columns).apply(
                lambda col: col.map(replace_nan)
            )

        if self.month_df.empty:
            # Creating dummy data for month_df
            num_rows = 10  # Number of rows for dummy data
            start_date = datetime.now().strftime(time_format)
            index = pd.date_range(
                end=start_date, periods=10, freq=monthly_frequency, name=index_name
            )
            self.month_df = pd.DataFrame(data=None, index=index, columns=columns).apply(
                lambda col: col.map(replace_nan)
            )

        if self.forever_df.empty:
            # Creating dummy data for forever_df
            time_index = pd.DatetimeIndex(pd.date_range(
                end=datetime.now(), periods=10, freq="D"
            ))
            time_index = time_index.strftime(forever_time_format)
            index = pd.MultiIndex.from_product(
                [time_index, ["max", "min", "mean", "median"]],
                names=forever_index_names,
            )
            self.forever_df =pd.DataFrame(
                data=None, index=index, columns=columns
            ).apply(lambda col: col.map(replace_nan))

    def write_to_daily(self, reading_file="reading.csv") -> pd.DataFrame:
        """
        Function that takes the last row of reading.csv and writes it to daily.csv.
        Checks if row has valid format (starts with < and ends with >)
            - adds a timestamp
            - deletes the <>
            - adds row to daily
         If format is not valid:
            - inserts row with nan
            - adds timestamp

        :param reading_file: File to read Data from insel
        :return: daily Dataframe
        """

        with open(reading_file, "r") as input_csv:
            data = input_csv.readlines()
        last_row = data[-1]
        first_col = str(last_row[0])
        last_col = str(last_row[-1])
        if first_col.startswith("<") and last_col.endswith(">"):
            last_row[0], last_row[-1] = (first_col.replace("<", ""),)
            last_col.replace(">", "")
            last_row = [last_row]
        else:
            print("Format not valid")
            last_row = None
        pd.concat(
            [
                self.daily_df,
                pd.DataFrame(
                    data=last_row,
                    columns=self.columns,
                    index=[datetime.now().strftime(self.time_format)],
                ),
            ]
        )

    def daily_cleanup(
        self, daily_file="daily.csv", monthly_file=None, forever_file="forever.csv"
    ):
        """
        Method to be called once a day to delete daily data and write to monthly and forever file
        :param daily_file:
        :param monthly_file:
        :param forever_file:
        :return:
        """
        if monthly_file == None:
            monthly_name = datetime.today().strftime("%b%Y")
            monthly_file = monthly_name + ".csv"

        self.write_to_forever(daily_file, forever_file)
        self.write_to_monthly(monthly_file, daily_file)

    def write_to_forever(self):
        """
        A method that writes the mean, median, max and min of the day for every variable to the forever file
        :param daily_file:
        :param forever_file:
        :return:
        """
        # make description df
        descibe = self.daily_df.describe()
        days = np.unique(self.daily_df.index.strftime("%d"))
        if len(days) == 1:
            date_index = pd.DatetimeIndex(np.unique(self.daily_df.index.strftime(self.forever_time_format))).strftime(self.forever_time_format)
        descibe.index = pd.MultiIndex.from_product([date_index, descibe.index], names=self.forever_index_names)
        self.forever_df = pd.concat([self.forever_df, descibe])
        return self.forever_df

    def write_to_monthly(self) -> pd.DataFrame:
        """
        Method that writes 48 new datapoints to the monthly file and automatically updates the mean,median,max,min header
        according to the new data
        :param monthly_file:
        :param daily_df:
        :return:
        """
        return pd.concat(
            [self.month_df, self.daily_df.resample(self.monthly_frequency).mean()]
        )


if __name__ == "__main__":
    test = InselDataframes()
    test.write_to_daily(reading_file="../Webserver/reading.csv")
    test.write_to_monthly()
    test.write_to_forever()

    # test.daily_cleanup(daily_file='new_daily.csv',
    #                      monthly_file='Jan2024.csv',
    #                      forever_file='forever.csv')
    # # write_to_daily('/home/julien/Desktop/Inselfitness/dataframe/reading_test.csv', '/home/julien/Desktop/Inselfitness/dataframe/daily.csv')
