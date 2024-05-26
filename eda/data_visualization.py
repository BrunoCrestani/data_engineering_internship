import streamlit as st
import pandas as pd
import os

def load_cleaned_data(directory):
    cleaned_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                filename = os.path.join(root, file)
                df = pd.read_csv(filename)
                cleaned_data[file] = df
    return cleaned_data

def main():
    st.title('Data Visualization with Streamlit')

    # Load cleaned data
    cleaned_data_dir = os.path.join(os.getcwd(), 'cleaned_csv_files')
    cleaned_data = load_cleaned_data(cleaned_data_dir)

    # Display each cleaned DataFrame
    for filename, df in cleaned_data.items():
        st.header(filename)
        st.write(df)

if __name__ == "__main__":
    main()

