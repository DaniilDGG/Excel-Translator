# Excel Translator with DeepL API

This Python script automates the process of translating content in an Excel file using the DeepL API. It supports multiple output languages, tracks progress for each step, and handles intermediate saves to prevent data loss during execution.

## Features

- **Translate Excel columns**: Automatically translate text from one language to multiple target languages.
- **Multiple output languages**: Specify any number of target languages in the configuration file.
- **Progress tracking**: Displays translation progress using `tqdm`.
- **Intermediate saves**: Saves results after every translation batch to ensure no progress is lost.
- **Configurable settings**: Easily adjust API keys, input/output languages, and other settings via a `config.txt` file.

## Requirements

- Python 3.7 or higher
- Required libraries: `pandas`, `requests`, `tqdm`

Install the required dependencies using:

```bash
pip install pandas requests tqdm
