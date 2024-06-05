import os
import pandas as pd

class DataCleaning:
    def __init__(self, project_dir):
        self.data_dir = project_dir 
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"The directory {self.data_dir} does not exist.")
        print(f"Initialized DataCleaning with directory: {self.data_dir}")

    # Method to load the files into the dataframes
    def load_csv_files(self):
        csv_files = []
        # Iterates through the directories
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))

        dataframes = {file: pd.read_csv(file) for file in csv_files}
        print(f"Loaded {len(dataframes)} CSV files.")
        return dataframes

    # Method to clean useless data
    def clean_data(self, dataframe):
        # Excludes empty lines
        dataframe = dataframe.dropna(how='all')
        dataframe = dataframe.dropna(axis=1, how='all')

        # Makes columns names prettier
        dataframe.columns = dataframe.columns.str.strip().str.lower().str.replace('_ ', ' ')

        # Check and remove the last row if it starts with specific words
        last_row_first_item = str(dataframe.iloc[-1, 0]).strip()
        if not last_row_first_item or last_row_first_item.startswith(("Fonte", "Nota", "(")):
            print(f"last row removed: {last_row_first_item}")
            dataframe = dataframe.iloc[:-1, :]
        
        return dataframe

    # Method to separate a sheet with 2 tables in diferent dataframes
    def separate_sheets(self, dataframe):
        # Arrray of found tables in the dataframes
        array = [col for col in dataframe.columns if col.startswith('tab')]
       
        # Verifies if there is more than 1
        if len(array) < 2:
            return [dataframe]
        else:
            # Separates the tables
            start_column = array[1]
            index = dataframe.columns.get_loc(start_column)
            new_df = dataframe.iloc[:, index:].copy()
            dataframe = dataframe.iloc[:, :index]

            dataframes = [dataframe, new_df]
            return dataframes

    # Method to reorganize the files and Tables names
    def reorganize_dfs(self, dataframes):
        # Iterates through dataframes looking for the ones to be separated
        for file_path, df in dataframes.items():
            separated_dfs = self.separate_sheets(df)
            # Defining the paths of the original file for use
            directory = os.path.dirname(file_path)
            base_filename = os.path.basename(file_path)
            filename_without_extension = os.path.splitext(base_filename)[0]

            # Correcting files names
            if filename_without_extension.endswith(' '):
                filename_without_extension = filename_without_extension[:-1]

            print(f"Filename without extension: {filename_without_extension}")

            # Process to correct the name of the arrays with separated dfs received
            if len(separated_dfs) > 1:
                if ' e ' in filename_without_extension:
                    file_name_parts = filename_without_extension.split(' e ')
                    print(f"Split into: {file_name_parts}")
                    part1_path = os.path.join(directory, file_name_parts[0] + '.csv')
                    part2_path = os.path.join(directory, file_name_parts[1] + '.csv')
                    separated_dfs[0].to_csv(part1_path, index=False)
                    separated_dfs[1].to_csv(part2_path, index=False)
                    print(f"Saved split files to: {part1_path}, {part2_path}")
                elif ' a ' in filename_without_extension:
                    file_name_parts = filename_without_extension.split(' a ')
                    print(f"Split into: {file_name_parts}")
                    part1_path = os.path.join(directory, file_name_parts[0] + '.csv')
                    part2_path = os.path.join(directory, file_name_parts[1] + '.csv')
                    separated_dfs[0].to_csv(part1_path, index=False)
                    separated_dfs[1].to_csv(part2_path, index=False)
                    print(f"Saved split files to: {part1_path}, {part2_path}")

                os.remove(file_path)
            else:
                print(f"No split needed for: {file_path}")
                separated_dfs[0].to_csv(file_path, index=False)
                print(f"Saved file to: {file_path}")

    # Save the csv cleaned files
    def save_clean_data(self, dataframes):
        # Iterates over the dataframes
        for file_path, df in dataframes.items():
            # Clean the DataFrame
            clean_df = self.clean_data(df)
            # Saves the dataframe
            clean_df.to_csv(file_path, index=False)
            print(f"Saved cleaned data to: {file_path}")

def main():
    data_dir = os.path.join(os.getcwd(), 'csv_files')
    project_dir = data_dir

    cleaner = DataCleaning(project_dir)
    dataframes = cleaner.load_csv_files()

    cleaned_dataframes = {filename: cleaner.clean_data(df) for filename, df in dataframes.items()} 

    saved_dataframes = cleaner.save_clean_data(cleaned_dataframes)
    cleaner.reorganize_dfs(cleaned_dataframes)

if __name__ == "__main__":
    main()

