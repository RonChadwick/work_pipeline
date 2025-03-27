# Basic validation checks  
import os  

def validate_pdf(file_path):  
    if not file_path.endswith('.pdf'):  
        raise ValueError("Not a PDF file")  
    if not os.path.exists(file_path):  
        raise FileNotFoundError(f"Missing file: {file_path}")  