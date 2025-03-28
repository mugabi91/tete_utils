# tete_utils

`tete_utils` is a Python utility repository designed to streamline data processing, encoding retrieval, and multiple-choice question analysis. It provides a collection of helper functions to enhance workflow efficiency when working with structured data, particularly in survey analysis and data transformation.

## Features

### 1. **Encoding Fetching Utility**
   - Retrieves encoding labels from XLSForm questions.
   - Caches Excel sheets to optimize repeated lookups.
   - Supports both string and numeric encodings.

### 2. **Multiple-Choice Question Analyzer**
   - Mimics Stata’s `mrtab` command.
   - Analyzes multiple-choice responses and summarizes them in an Excel report.

### 3. **More utilities coming soon!**
   - Additional tools for data cleaning, transformation, and statistical analysis will be added over time.

## Installation

Clone the repository:
```bash
git clone https://github.com/mugabi91/tete_utils
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Example: Encoding Fetching
```python
from tete_utils.tete_utils import get_encoding_dict

file_path = "survey_data.xlsx"
encoding_dict = get_encoding_dict("q1_choices", file_path)
print(encoding_dict)
```

## Contributing

Contributions are welcome! If you have additional utilities to contribute, feel free to submit a pull request.

## License

This repository is licensed under the MIT License.
