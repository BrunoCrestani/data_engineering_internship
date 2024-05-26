import os
import pandas as pd

class Converter:

    def __init__(self, input_path, output_path):
        self.input_path = input_path 
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    # method to convert a downloaded xslx file into a csv file 
    def csv_converter(self):

        for filename in os.listdir(self.input_path):
            #defining input path for the file  
            file_path = os.path.join (self.input_path, filename)
            xslx_file = pd.ExcelFile(file_path)
       
            for sheet_name in xslx_file.sheet_names:
                #making a dataframe from the xslx file 
                dataframe = pd.read_excel(file_path, sheet_name=sheet_name)

                if not dataframe.empty:
                    filename_dir = os.path.splitext(filename)[0]

                    dir_path = os.path.join(self.output_path, filename_dir)
                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    # defining the output path for the file
                    csv_file_name = f"{sheet_name}.csv"
                    csv_file_path = os.path.join(dir_path, csv_file_name)

                    #converting the dataframe in the output to a csv file
                    dataframe.to_csv(csv_file_path, index=False)
                    print(f'Converted {csv_file_name}')
