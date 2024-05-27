import os
import streamlit as st
import pandas as pd

class DataVisualizer:

    def __init__(self, cleaned_data_dir, data_example):
        self.cleaned_data_dir = cleaned_data_dir
        self.data_example = data_example

    # method to example a visualization of a treated sheet
    def visualize_data(self):

        #treating sheet specifically
        df = pd.read_csv(self.data_example)
        st.title = (df.iloc[0,0])
        st.subheader(df.iloc[0,1])

        df = pd.read_csv(self.data_example, skiprows=3)

        column0 = df.columns[0]
        column1 = df.columns[1]
        
        df.rename(columns={column0: ''}, inplace=True)
        df.rename(columns={column1: 'Brasil'}, inplace=True)
        st.write(df)

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

    def display_sheets(self):

        plt.switch_backend('TkAgg')
        st.title('Data Visualization with Streamlit')

        # Load cleaned data
        cleaned_data = self.load_cleaned_data()

        # Display each cleaned DataFrame
        for filename, df in cleaned_data.items():
            st.header(filename)
            st.write(df)

def main():

    cleaned_data_dir = os.path.join(os.getcwd(), 'cleaned_csv_files')
    data_example = os.path.join(cleaned_data_dir, 'Tab 1.1.18.3.csv')
    
    data_visualizer = DataVisualizer(cleaned_data_dir, data_example)
    data_visualizer.visualize_data()

if __name__ == "__main__":
    main()


