import pandas as pd 
from typing import List
import os 

def load_data(file_location:str|None, sheet_name:str|None=None)-> pd.DataFrame:
    if file_location is None:
        raise ValueError("Please provide a file location")
    df = pd.read_excel(file_location, sheet_name=sheet_name) #type:ignore
    print(df.head(5)) #type:ignore
    return df  #type:ignore



def filter_data(df:pd.DataFrame, interested_col:str)-> pd.DataFrame:
    """Filters the dataframe and retuerns the columns that start with the interested column
    Dont forget to add the forward slash at the end of the interested column eg "Has_Chronic_disease/"

    Args:
        df (pd.DataFrame): Dataframe to be filtered
        interested_col (str): Column to be filtered

    Returns:
        pd.DataFrame: _description_
    """
    cols: List[str] = [i for i in df.columns if i.startswith(interested_col)]
    return df[cols]

    
def mr_tab(df:pd.DataFrame)->pd.DataFrame:
    """Generates a frequency table for the dataframe

    Args:
        df (pd.DataFrame): dataframe to be used

    Returns:
        pd.DataFrame: Frequency table
    """
    cases = df.shape[0]
    Total_Response = sum(df.sum(axis=0).reset_index()[0].to_list()) #type:ignore
    return_df = df.sum(axis=0).reset_index().rename(columns={"index":"Choice", 0:"Frequency"}) #type:ignore
    return_df["Response Percentage"] =round((return_df["Frequency"]/Total_Response), 4) #type:ignore
    return_df["Case Percentage"] = round((return_df["Frequency"]/cases), 4) #type:ignore
    return return_df



def get_mr_table_by(df:pd.DataFrame, index_col:str|list[str], value_columns:list[str]|str)->pd.DataFrame:
    """Gets the multi repsonce table for the given columns and given catergorical columns

    Args:
        df (pd.DataFrame): dataframe to be used
        index_col (str | list[str]):column to be used as index
        value_columns (list[str | str]): multi choice question columns

    Returns:
        pd.DataFrame: multi response table
    """
    df = pd.pivot_table(df, index=index_col, values=value_columns, aggfunc="sum").T #type:ignore
    df["Total_Response"] = df.sum(axis=1) #type:ignore
    for col in df.columns:
        if col not in ["Total_Response",index_col]:
            df[col] = df[col] / df["Total_Response"]
    return df 


def save_to_excel(df:pd.DataFrame, sheet_name:str):
    """Saves the dataframe to an excel file

    Args:
        df (pd.DataFrame): Dataframe to be saved
        file_name (str): Name of the file to be saved
    """
    if os.path.exists(r"C:\Users\M D\Desktop\tete_utils\Multichoice_analysis_results.xlsx"):
        with pd.ExcelWriter(r"C:\Users\M D\Desktop\tete_utils\Multichoice_analysis_results.xlsx", mode="a", engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name= f"{sheet_name.split('/')[0]}", index=True) # type:ignore
    else:
        with pd.ExcelWriter(r"C:\Users\M D\Desktop\tete_utils\Multichoice_analysis_results.xlsx", engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name= f"{sheet_name.split('/')[0]}", index=True) # type:ignore
        
        
def main(interested_catergory:str|list[str]|None=None) -> None:
    
    MAIN_DF = load_data(file_location=DATA_FILE, sheet_name=f"{SHEET_NAME}")
    print("\n\n")
    for col in MULTI_CHOICE_COLUMNS:
        filtered_df = filter_data(MAIN_DF, col)
        print(mr_tab(filtered_df))
        print("\n\n")
        save_to_excel(mr_tab(filtered_df), col)
        
        if interested_catergory is not None :
            if isinstance(interested_catergory, str):
                print(get_mr_table_by(df=MAIN_DF,  index_col=interested_catergory, value_columns=filtered_df.columns.to_list()))
                print("\n\n")
                save_to_excel(get_mr_table_by(df=MAIN_DF,  index_col=interested_catergory, value_columns=filtered_df.columns.to_list()), f"{interested_catergory}_{col}")
                
            else:
                for i in interested_catergory:
                    print(get_mr_table_by(df=MAIN_DF,  index_col=i, value_columns=filtered_df.columns.to_list()))
                    print("\n\n")
                    save_to_excel(get_mr_table_by(df=MAIN_DF,  index_col=i, value_columns=filtered_df.columns.to_list()), f"{i}_{col}")
        
if __name__ == "__main__":
    DATA_FILE = r"D:\movie centre\RAP_test_-_all_versions_-_False_-_2024-12-17-15-59-30.xlsx"
    SHEET_NAME = "collect_names"
    MULTI_CHOICE_COLUMNS = ["Has_Chronic_disease/","Has_Disabililty/","Extra_income_sources/"]
    main(["Gender","Marital_status"]) #type:ignore
    
    ### read me ###
    """
    Feed this script the file location of your data, the sheet on which its on (reads only excels files)
    Feed it as has the start name of the variable of the multichoice question say you have variable 
    "Has_chronic_disease/" feed it all the multic choice question variables and dont forget to include the delimiter "/"
    eg mutichoice_cloumns = ["Has_Chronic_disease/","Has_Disabililty/"]
    If you would like to slice the output of these mutlichoice question results then  inculde the name of that categorical variable in 
    intereseted catergory argrument in main which takes either a list of variables or  a single variable...
    It will output an xlsx file called multic choice analysis results in your working dir
    """
    