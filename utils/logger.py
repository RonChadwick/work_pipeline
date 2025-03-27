# Simple error logging  
import logging  

def setup_logger():  
    logging.basicConfig(  
        filename='errors.log',  
        level=logging.ERROR,  
        format='%(asctime)s - %(levelname)s - %(message)s'  
    )  

def log_error(file_path, error):  
    logging.error(f"Failed to ingest {file_path}: {str(error)}")  