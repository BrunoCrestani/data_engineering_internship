import streamlit as st
import pandas as pd
import os

class DataVisualizer:

    def __init__(self, cleaned_data_dir):
        self.cleaned_data_dir = cleaned_data_dir

    def load_cleaned_data(self):
        cleaned_data = {}

        # Iterates through the directory
        for root, _, files in os.walk(self.cleaned_data_dir):
            for file in files:
                if file.endswith('.csv'):
                    filename = os.path.join(root, file)
                    df = pd.read_csv(filename)
                    cleaned_data[file] = df
        return cleaned_data

    def display_data(self):
        st.title('Data Visualization with Streamlit')

        # Load cleaned data
        cleaned_data = self.load_cleaned_data()

        # Display each cleaned DataFrame
        for filename, df in cleaned_data.items():
            st.header(filename)
            st.write(df)

def main():
    cleaned_data_dir = os.path.join(os.getcwd(), 'cleaned_csv_files')
    data_visualizer = DataVisualizer(cleaned_data_dir)
    data_visualizer.display_data()

if __name__ == "__main__":
    main()

