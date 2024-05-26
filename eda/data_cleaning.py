import os
import pandas as pd

class DataCleaning:

    def __init__(self, project_dir):
        self.data_dir = project_dir 
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"O diretorio {self.data_dir} nao existe.")

    # method to load the files into the dataframes
    def load_csv_files(self):
        csv_files = []

        #iterates through the directories
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))

        dataframes = {os.path.basename(file): pd.read_csv(file) for file in csv_files}
        return dataframes

    # methods to clean useless data
    def clean_data(self, dataframe):


        # excludes empty lines
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.dropna(axis=1, how='all')

        # makes columns names prettier
        dataframe.columns = dataframe.columns.str.strip().str.lower().str.replace('_ ', ' ')

        return dataframe

    #save the csv cleaned files
    def save_clean_data(self, dataframes, output_dir):
        # verifies if the output directory already existis
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterates over the dataframes
        for filename, df in dataframes.items():

            relative_path = os.path.relpath(filename, start=self.data_dir)
            
            # Clean the DataFrame
            clean_df = self.clean_data(df)
            # Saves the dataframe
            clean_df.to_csv(os.path.join(output_dir, os.path.basename((filename))), index=False)

def main():
    data_dir = os.path.join(os.getcwd(), 'csv_files')
    project_dir = data_dir
    output_dir = os.path.join(os.getcwd(), 'cleaned_csv_files')

    cleaner = DataCleaning(project_dir)
    dataframes = cleaner.load_csv_files()

    cleaned_dataframes = {filename: cleaner.clean_data(df) for filename, df in dataframes.items()} 
    
    cleaner.save_clean_data(cleaned_dataframes, output_dir)

if __name__ == "__main__":
    main()
