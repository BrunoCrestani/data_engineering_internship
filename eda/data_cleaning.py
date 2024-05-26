import os
import pandas as pd

class DataCleaning:

    def __init__(self, project_dir):
        self.data_dir = project_dir 
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"O diretorio {self.data_dir} nao existe.")

    def load_csv_files(self):
        csv_files = []

        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))

        dataframes = {os.path.basename(file): pd.read_csv(file) for file in csv_files}
        return dataframes

    def clean_data(self, dataframe):
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.dropna(axis=1, how='all')

        dataframe.fillna(0, inplace=True)

        dataframe.columns = dataframe.columns.str.strip().str.lower().str.replace(' ', '_')

        return dataframe
 
    def save_clean_data(self, dataframes, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename, df in dataframes.items():

            subdirectory = os.path.dirname(filename)
            print(subdirectory)
            
            output_subdir = os.path.join(output_dir, subdirectory)

            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)

            clean_df = self.clean_data(df)
            clean_df.to_csv(os.path.join(output_dir, filename), index=False)


if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), 'csv_files')
    project_dir = data_dir
    output_dir = os.path.join(os.getcwd(), 'cleaned_csv_files')

    cleaner = DataCleaning(project_dir)
    dataframes = cleaner.load_csv_files()

    cleaned_dataframes = {filename: cleaner.clean_data(df) for filename, df in dataframes.items()} 
    
    cleaner.save_clean_data(cleaned_dataframes, output_dir)
