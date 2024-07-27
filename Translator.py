import pandas as pd
import requests
from tqdm import tqdm

def load_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            if ': ' in line:
                key, value = line.strip().split(': ', 1)
                if key == 'Output_Langs':
                    config[key] = value.split(', ')
                else:
                    config[key] = value
    return config

def deepl_translate(text, target_lang, api_key):
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "text": text,
        "target_lang": target_lang.upper(),
        "auth_key": api_key
    }

    response = requests.post(url, data=data)

    try:
        response.raise_for_status()  # Check for errors in the response

        translation = response.json()['translations'][0]['text']
        return translation
    except (KeyError, requests.exceptions.HTTPError) as e:
        print(f"Error translating text: {text}. Error: {e}")
        return 'Translation Error'

def find_column_by_value(df, value):
    for column in df.columns:
        if str(column).strip().lower() == value.strip().lower():
            return column
    return None

def print_first_rows_of_columns(df):
    print("Content of the first rows of all non-empty columns:")
    for column in df.columns:
        if df[column].count() > 0:  # Check if column is not empty
            print(f"{column}: {df[column].iloc[:5].tolist()}")  # Print first 5 rows of the column

config = load_config()

API_KEY = config['API_KEY']
input_lang = config['Input_Lang']
output_langs = config['Output_Langs']

# Ask user for the Excel file name
excel_file = input("Enter the Excel file name to translate (including extension): ")

# Load Excel file
df = pd.read_excel(excel_file)

# Find the column with the input language in the first row
input_column = find_column_by_value(df, input_lang)
if input_column is None:
    print(f"Column with '{input_lang}' not found")
    print_first_rows_of_columns(df)
    exit()

for output_lang in output_langs:
    target_column = find_column_by_value(df, output_lang)
    if target_column is None:
        target_column = output_lang
        df[target_column] = ''

    # Split translation into 4 parts (25% each)
    num_rows = len(df)
    step = num_rows // 4

    for i in range(4):
        start = i * step
        end = (i + 1) * step if i < 3 else num_rows

        tqdm_desc = f"Translating to {output_lang} - Progress: {int((end / num_rows)*100)}%"
        tqdm.pandas(desc=tqdm_desc, position=i)
        df.loc[start:end, target_column] = df.loc[start:end, input_column].progress_apply(lambda x: deepl_translate(x, output_lang, API_KEY))

        # Save intermediate results
        if i < 3:
            df.to_excel('translated_file.xlsx', index=False)

# Save the final results back to an Excel file
df.to_excel('translated_file.xlsx', index=False)

