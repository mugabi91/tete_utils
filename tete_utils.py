
import pandas as pd

def read_data(file_location:str|None,sheet_name:str|None) -> pd.DataFrame|None:
    if file_location is not  None and sheet_name is not None:
        df = pd.read_excel(file_location,sheet_name=sheet_name) # type:ignore 
        df.columns = [col_name.strip() for col_name in df.columns]
        return df
    else:
        raise ValueError("[ERROR_INFO]>>> File location or sheet_name were not provided...")
    
def get_list_names(df:pd.DataFrame):
    if "list_name" in df.columns:
        return df["list_name"].unique().tolist() #type:ignore

def filter_df(df:pd.DataFrame,filter_option:str):
    if filter_option in get_list_names(df): # type:ignore
        return df.query("list_name == @filter_option")[["name","label"]] #type: ignore
    else:
        raise KeyError(" [ERROR_INFO]>> The filter option used doesnt exist in the 'list_name' column...")

def get_encoding_dict(selection_option:str, file_location:str ,sheet_name:str="choices",encodings_type:str="str"): #type:ignore
    """ This function retrieves the encoding labels of  a given selection  option and returns a dict 
    Args:
        selection_option (str): selection option used in the questionnaire design
        file_location (str): location of the file 
        sheet_name (str, optional): sheet name where the encoding are Defaults to "choices".
        encodings_type(str, optional) "str" or "number" The data trying to be encoded.decoded is it in str or numeric format.
    """
    return_dict = {}
    dataframe: pd.DataFrame | None = read_data(file_location=file_location, sheet_name=sheet_name)
    df_Filtered = filter_df(dataframe,selection_option) # type:ignore
    for name, label in zip(df_Filtered.name, df_Filtered.label): #type:ignore
        if encodings_type == "str":
            temp_dict = {  #type:ignore
                name:label
            }
            return_dict.update(temp_dict)  #type:ignore
        else:
            temp_dict = {  #type:ignore
                int(x=name):label  #type:ignore
            }
            return_dict.update(temp_dict)  #type:ignore
            
    return return_dict  #type:ignore
        

if __name__ =="__main__":
    print("Running main")