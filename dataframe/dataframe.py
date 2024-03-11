import pandas as pd 
import csv
from datetime import datetime, date


class InselDataframes():
    def __init__(self):
        self.daily_df = None

    

    def write_to_daily(self, reading_file = 'reading.csv', daily_file = 'daily.csv'):
        '''Function that takes the last row of reading.csv and writes it to daily.csv. If row has valid format 
        (starts with < and ends with >), adds a timestamp, deletes the <> and copies the row. If format is not valid,
        copies a row full, writes a row with timestamp 66:66:66 and other columns NA'''
        with open(reading_file, "r") as input_csv, open(daily_file, 'a') as output_csv:
            csv_reader, csv_writer = csv.reader(input_csv, delimiter=","), csv.writer(output_csv, delimiter=',')
            for row in csv_reader:
                last_row = row        #iterate through all the rows until we get to the last one
            first_col = str(last_row[0])
            last_col = str(last_row[-1])
            timestamp = datetime.today().strftime('%d/%m/%Y-%H:%M:%S')
            if first_col.startswith('<') and last_col.endswith('>'):
                last_row[0] , last_row[-1]= first_col.replace('<',''), last_col.replace('>', '')  #delete the < >                                 
                last_row.insert(0, timestamp)                    #add timestamp
            else:
                print("Format not valid")       
                for i in range(len(last_row)):      #write a colum with only N/A
                    last_row[i] = 'NA'
                last_row.insert(0, 'NA')
            csv_writer.writerow(last_row)   


    def daily_cleanup(self, daily_file = 'daily.csv', monthly_file =None, forever_file='forever.csv'):
        '''
        Method to be called once a day. '''
        if monthly_file == None:
            monthly_name = datetime.today().strftime('%b%Y')
            monthly_file = monthly_name + '.csv'

        self.write_to_forever(daily_file, forever_file)
        self.write_to_monthly(monthly_file, daily_file)
        

    def make_4m_df(self, input_df:pd.DataFrame) -> pd.DataFrame :
        '''Creates a 4x12 dataframe indicating the results of measures of central tendencies on the input dataframe.
        Input dataframe must be a 
        The output dataframe is defined as follows : 
        rows [mean,median,max,min]
        columns [measure, Cpv, Cwt, Cwr, Cg, Cbp, Cbn, vw, Dw, Is, Ta, Tb, Vb] 
        '''

        row_names = ['max','min','mean', 'median']
        column_names = ["measure", "Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]
        result_df = pd.DataFrame(columns = column_names, index=row_names)


        for col in column_names: 
                if col == 'measure' : #we only want the columns Cpv ..... Vb
                    result_df[col] = row_names
                else:
                    result_df.loc['mean', col] = input_df[col].mean()
                    result_df.loc['max', col] = input_df[col].max()
                    result_df.loc['min', col] = input_df[col].min()
                    result_df.loc['median', col] = input_df[col].median()

        return result_df

    def write_to_forever(self, daily_file, forever_file):
        '''
        A method that writes the mean, median, max and min of the day for every variable to the forever file
        '''
        
        column_names = ["timestamp", "Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]
        daily_df = pd.read_csv(daily_file, names = column_names)
        initial_row_number = daily_df.shape[0]
        daily_df.drop(daily_df[daily_df.timestamp == '66/66/6666-66:66:66'].index, inplace=True)  #get rid of the colums starting with 66:66:66 (invalid format marker)
        daily_df.reset_index(inplace=True, drop=True)                                   #reindex the rows from 0 to X
        final_row_number = daily_df.shape[0]
        print(f"{initial_row_number - final_row_number} rows had an incorrect format and were ignored")
        self.daily_df = daily_df #save as an attribute so that write_to_monthly can also use it

        result_column_names = ["date", "measure", "Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]

        result_df =self.make_4m_df(daily_df)
        date = datetime.today().strftime('%d/%m/%Y')
        result_df.insert(0, 'date', date)



        result_df.to_csv(forever_file, sep=',', header=result_column_names, index=False, mode='a')
    
    def write_to_monthly(self,monthly_file, daily_df):
        '''
        Method that writes 48 new datapoints to the monthly file and automatically updates the mean,median,max,min header
        according to the new data'''
        column_names = ["measure", "Cpv", "Cwt", "Cwr", "Cg", "Cbp", "Cbn", "vw", "Dw", "Is", "Ta", "Tb", "Vb"]
        monthly_df = pd.read_csv(monthly_file, names = column_names, header=4)
        ####we want to keep 48 (2 per hour) datapoints per day for every day in the monthly_file
        ####assuming we are sampling data every 5min, we need to keep one line in 6 to keep every 30min
        add_to_monthly_df = daily_df.copy(deep=True)
        for i in range(daily_df.shape[0]):
            if i%6 != 0:
                add_to_monthly_df.drop(i, inplace=True)

        updated_monthly_df = pd.concat([monthly_df, add_to_monthly_df])  #add the daily 48 datapoints to the monthly file
        result_df_2 = self.make_4m_df(updated_monthly_df)       #calculate the new total median, mean, max, min
        result_df_2.rename(columns={'measure' : 'timestamp'}, inplace=True)
        updated_monthly_df = pd.concat([result_df_2, updated_monthly_df])  #add the 4 rows of result_df_2 at the top 
        updated_monthly_df.to_csv(monthly_file, sep=',', header=column_names, index=False,mode='w')




if __name__ == "__main__":
    test = InselDataframes()
    test.daily_cleanup(daily_file='/home/julien/Desktop/Inselfitness/dataframe/new_daily.csv', 
                         monthly_file='/home/julien/Desktop/Inselfitness/dataframe/Jan2024.csv', 
                         forever_file='/home/julien/Desktop/Inselfitness/dataframe/forever.csv')
    # write_to_daily('/home/julien/Desktop/Inselfitness/dataframe/reading_test.csv', '/home/julien/Desktop/Inselfitness/dataframe/daily.csv')


