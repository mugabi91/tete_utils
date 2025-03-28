import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ExcelCache:
    _cache = None
    _last_modified = None

    @classmethod
    def get_sheet(cls, file_location: str, sheet_name: str) -> pd.DataFrame | None:
        if not os.path.exists(file_location):
            logging.error("File does not exist: %s", file_location)
            raise FileNotFoundError(f"File not found: {file_location}")
        
        modified_time = os.path.getmtime(file_location)
        
        # Reload if file has changed or cache is empty
        if cls._cache is None or modified_time != cls._last_modified:
            logging.info("Loading Excel file: %s", file_location)
            cls._cache = pd.read_excel(file_location, sheet_name=None)  # Read all sheets into memory
            cls._last_modified = modified_time

        if sheet_name not in cls._cache:
            logging.error("Sheet not found: %s", sheet_name)
            raise KeyError(f"Sheet '{sheet_name}' not found in the file.")
        
        return cls._cache[sheet_name]

def get_list_names(df: pd.DataFrame):
    if "list_name" in df.columns:
        return df["list_name"].unique().tolist()
    logging.error("'list_name' column not found in DataFrame")
    raise KeyError("'list_name' column not found in DataFrame")

def filter_df(df: pd.DataFrame, filter_option: str):
    if filter_option in get_list_names(df):
        return df.query("list_name == @filter_option")[["name", "label"]]
    logging.error("Filter option '%s' not found in 'list_name' column", filter_option)
    raise KeyError(f"Filter option '{filter_option}' not found in 'list_name' column")

def get_encoding_dict(selection_option: str, file_location: str, sheet_name: str = "choices", encodings_type: str = "str") -> dict:
    """
    Retrieves the encoding labels of a given selection option and returns a dictionary.
    
    Args:
        selection_option (str): Selection option used in the questionnaire design.
        file_location (str): Location of the Excel file.
        sheet_name (str, optional): Sheet name where the encoding is stored. Defaults to "choices".
        encodings_type (str, optional): "str" for string encoding, "number" for numeric encoding.
    """
    try:
        dataframe = ExcelCache.get_sheet(file_location, sheet_name)
        df_filtered = filter_df(dataframe, selection_option)
        return_dict = {}
        
        for name, label in zip(df_filtered.name, df_filtered.label):
            if encodings_type == "str":
                return_dict[name] = label
            else:
                return_dict[int(name)] = label  # Ensure numeric encoding
                
        return return_dict
    
    except (KeyError, FileNotFoundError) as e:
        logging.error("Error retrieving encoding dictionary: %s", e)
        return {}  # Return empty dict on error

if __name__ == "__main__":
    logging.info("Main execution started")
