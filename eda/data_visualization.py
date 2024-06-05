import os
import streamlit as st
import pandas as pd

class DataVisualizer:
    def __init__(self, cleaned_data_dir):
        self.cleaned_data_dir = cleaned_data_dir

    # Method to visualize a specific example sheet
    def visualize_data_example(self, data_example):
        # Load the example CSV file
        df = pd.read_csv(data_example)
        
        # Set the title and subheader
        st.title(df.iloc[0, 0])
        st.subheader(df.iloc[0, 1])

        # Reload the DataFrame skipping the first three rows
        df = pd.read_csv(data_example, skiprows=3)

        # Rename columns
        column0 = df.columns[0]
        column1 = df.columns[1]
        
        df.rename(columns={column0: '', column1: 'Brasil'}, inplace=True)
        st.write(df)

    def load_cleaned_data(self):
        cleaned_data = {}

        # Iterates through the directory to load cleaned data
        for root, _, files in os.walk(self.cleaned_data_dir):
            for file in files:
                if file.endswith('.csv'):
                    filename = os.path.join(root, file)
                    df = pd.read_csv(filename)
                    cleaned_data[file] = df
        return cleaned_data

    def display_sheets(self):
        st.title('Data Visualization with Streamlit')

        # Load cleaned data
        cleaned_data = self.load_cleaned_data()

        # Display each cleaned DataFrame
        for filename, df in cleaned_data.items():
            st.subheader(f'Data from {filename}')
            st.write(df)

def main():
    cleaned_data_dir = os.path.join(os.getcwd(), 'csv_files')
    data_example = os.path.join(cleaned_data_dir, 'Tab 1.1.18.3.csv')
    
    data_visualizer = DataVisualizer(cleaned_data_dir)
    data_visualizer.display_sheets()

if __name__ == "__main__":
    main()

