from dotenv import load_dotenv
import os
from scripts.pensum_tui import logging


def load_env(env_path:str, variable_name:str):
    """Load environment variables from a .env file."""
    try:
        load_dotenv(env_path)
        env_variable = os.getenv(variable_name)
        return env_variable if env_variable else None
    except Exception as e:
        logging.error(f"Error loading environment variable '{variable_name}': {e}")
        return None

def get_actual_file_to_load(file_name, data_folder):

    """Get the actual file to load, checking for updated CSV files if necessary."""
    # If it's a PDF, check if corresponding CSV updated file exists
    try:
        if file_name.endswith('.pdf'):
            base_name = os.path.splitext(file_name)[0]
            updated_csv = f"{base_name}_updated.csv"
            updated_csv_path = os.path.join(data_folder, updated_csv)
            if os.path.exists(updated_csv_path):
                return updated_csv  # Return filename only
        return file_name
    except Exception as e:
        logging.error(f"Error checking for updated CSV: {e}")
        return file_name


    


    
    
        

