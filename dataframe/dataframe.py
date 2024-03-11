import pandas as pd
import csv
from datetime import datetime, date
import numpy as np

'''
Todo:
    - Cleanup column names
    - Remove duplicate Headers
    - Seperate Methods and Init in InselDataframes()
    - relative paths
'''

def replace_nan(val):
    return val if not np.isnan(val) else np.random.choice([1, 3])

class InselDataframes():
    def __init__(self, daily_df: pd.DataFrame = pd.DataFrame(), forever_df: pd.DataFrame = pd.DataFrame(),
                 month_df: pd.DataFrame = pd.DataFrame()):

        columns = ["Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]
        forever_index_names = ["Date", "Type"]
        index_name = "Date"
        time_format = "%m/%d/%Y %H:%M"

        self.columns = columns
        self.time_format = time_format

        self.index_name = index_name
        self.forever_index_names = forever_index_names

        self.daily_df = daily_df
        self.month_df = month_df
        self.forever_df = forever_df

        if self.daily_df.empty:
            # Creating dummy data for daily_df
            index = pd.date_range(end=datetime.now().strftime(time_format), periods=13, freq='5min', name=index_name)
            self.daily_df = pd.DataFrame(data=None, index=index, columns=columns).apply(lambda col: col.map(replace_nan))

        if self.month_df.empty:
            # Creating dummy data for month_df
            num_rows = 10  # Number of rows for dummy data
            start_date = datetime.now().strftime(time_format)
            index = pd.date_range(end=start_date, periods=10, freq='D', name=index_name)
            self.month_df = pd.DataFrame(data=None, index=index,
                                         columns=columns).apply(lambda col: col.map(replace_nan))

        if self.forever_df.empty:
            # Creating dummy data for forever_df
            num_rows = 4  # Number of rows for dummy data
            start_date = datetime.now().strftime(time_format)
            index = pd.MultiIndex.from_product([[start_date], ['max', 'min', 'mean', 'median']],
                                               names=forever_index_names)
            self.forever_df = pd.DataFrame(data=None, index=index,
                                           columns=columns).apply(lambda col: col.map(replace_nan))

    def write_to_daily(self, reading_file='reading.csv') -> pd.DataFrame:
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

        with (open(reading_file, "r") as input_csv):
            data = input_csv.readlines()
        last_row = data[-1]
        first_col = str(last_row[0])
        last_col = str(last_row[-1])
        if first_col.startswith('<') and last_col.endswith('>'):
            last_row[0], last_row[-1] = first_col.replace('<', ''),
            last_col.replace('>','')
            last_row = [last_row]
        else:
            print("Format not valid")
            last_row = None
        pd.concat([self.daily_df, pd.DataFrame(data=last_row, columns=self.columns,
                                                   index=[datetime.now().strftime(self.time_format)])])

    def daily_cleanup(self, daily_file='daily.csv', monthly_file=None, forever_file='forever.csv'):
        """
        Method to be called once a day to delete daily data and write to monthly and forever file
        :param daily_file:
        :param monthly_file:
        :param forever_file:
        :return:
        """
        if monthly_file == None:
            monthly_name = datetime.today().strftime('%b%Y')
            monthly_file = monthly_name + '.csv'

        self.write_to_forever(daily_file, forever_file)
        self.write_to_monthly(monthly_file, daily_file)

    def make_4m_df(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates a 4x12 dataframe indicating the results of measures of central tendencies on the input dataframe.
        Input dataframe must be a
        The output dataframe is defined as follows :
        rows [mean,median,max,min]
        columns [measure, Cpv, Cwt, Cwr, Cg, Cbp, Cbn, vw, Dw, Is, Ta, Tb, Vb]
        :param input_df:
        :return:
        """
        row_names = ['max', 'min', 'mean', 'median']
        result_df = pd.DataFrame(columns=self.column_names, index=row_names)

        for col in self.column_names:
            if col == 'measure':  # we only want the columns Cpv ..... Vb
                result_df[col] = row_names
            else:
                result_df.loc['mean', col] = input_df[col].mean()
                result_df.loc['max', col] = input_df[col].max()
                result_df.loc['min', col] = input_df[col].min()
                result_df.loc['median', col] = input_df[col].median()

        return result_df

    def write_to_forever(self, daily_file, forever_file):
        """
        A method that writes the mean, median, max and min of the day for every variable to the forever file
        :param daily_file:
        :param forever_file:
        :return:
        """
        daily_df = pd.read_csv(daily_file, names=self.columns)
        initial_row_number = daily_df.shape[0]
        daily_df.drop(daily_df[daily_df.timestamp == '66/66/6666-66:66:66'].index,
                      inplace=True)  # get rid of the colums starting with 66:66:66 (invalid format marker)
        daily_df.reset_index(inplace=True, drop=True)  # reindex the rows from 0 to X
        final_row_number = daily_df.shape[0]
        print(f"{initial_row_number - final_row_number} rows had an incorrect format and were ignored")
        self.daily_df = daily_df  # save as an attribute so that write_to_monthly can also use it

        result_column_names = self.columns + ["date"]

        result_df = self.make_4m_df(daily_df)
        date = datetime.today().strftime('%d/%m/%Y')
        result_df.insert(0, 'date', date)

        result_df.to_csv(forever_file, sep=',', header=result_column_names, index=False, mode='a')

    def write_to_monthly(self, monthly_file, daily_df):
        """
        Method that writes 48 new datapoints to the monthly file and automatically updates the mean,median,max,min header
        according to the new data
        :param monthly_file:
        :param daily_df:
        :return:
        """
        column_names = ["measure", "Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]
        monthly_df = pd.read_csv(monthly_file, names=column_names, header=4)
        ####we want to keep 48 (2 per hour) datapoints per day for every day in the monthly_file
        ####assuming we are sampling data every 5min, we need to keep one line in 6 to keep every 30min
        add_to_monthly_df = daily_df.copy(deep=True)
        for i in range(daily_df.shape[0]):
            if i % 6 != 0:
                add_to_monthly_df.drop(i, inplace=True)

        updated_monthly_df = pd.concat(
            [monthly_df, add_to_monthly_df])  # add the daily 48 datapoints to the monthly file
        result_df_2 = self.make_4m_df(updated_monthly_df)  # calculate the new total median, mean, max, min
        result_df_2.rename(columns={'measure': 'timestamp'}, inplace=True)
        updated_monthly_df = pd.concat([result_df_2, updated_monthly_df])  # add the 4 rows of result_df_2 at the top
        updated_monthly_df.to_csv(monthly_file, sep=',', header=column_names, index=False, mode='w')


if __name__ == "__main__":
    test = InselDataframes()
    test.write_to_daily(reading_file="../Webserver/reading.csv")

    # test.daily_cleanup(daily_file='new_daily.csv',
    #                      monthly_file='Jan2024.csv',
    #                      forever_file='forever.csv')
    # # write_to_daily('/home/julien/Desktop/Inselfitness/dataframe/reading_test.csv', '/home/julien/Desktop/Inselfitness/dataframe/daily.csv')
