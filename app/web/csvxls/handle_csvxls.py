import pandas as pd 
from sqlalchemy import create_engine


def handle_csvxls(document_name, user_id, file_path, file_extension):
    engine = create_engine(f"sqlite:///instance/{user_id}_{document_name.split('.')[0]}.db")
    if file_extension == "csv":
        df = pd.read_csv(file_path)
    elif file_extension == "xlsx":
        df = pd.read_excel(file_path)
    else:
        return "Invalid file extension"
    df.to_sql(f"{document_name.split('.')[0]}", engine, if_exists="replace")
    
