import os  
import sqlite3  
import hashlib  
import json  
from PyPDF2 import PdfReader  
from utils.logger import setup_logger, log_error  
from utils.validator import validate_pdf  

def get_checksum(file_path):  
    with open(file_path, 'rb') as f:  
        return hashlib.sha256(f.read()).hexdigest()  

def extract_pdf_metadata(file_path):  
    try:  
        with open(file_path, 'rb') as f:  
            reader = PdfReader(f)  
            return {  
                "num_pages": len(reader.pages),  
                "author": reader.metadata.get('/Author', ''),  
                "title": reader.metadata.get('/Title', '')  
            }  
    except Exception as e:  
        log_error(file_path, e)  
        return {}  

def ingest_pdf(file_path):  
    setup_logger()  
    try:  
        validate_pdf(file_path)  
        checksum = get_checksum(file_path)  

        # Connect to database  
        conn = sqlite3.connect('data/files.db')  
        cursor = conn.cursor()  

        # Check for duplicates  
        cursor.execute('SELECT id FROM files WHERE checksum=?', (checksum,))  
        if cursor.fetchone():  
            print(f"Skipping duplicate: {file_path}")  
            return  

        # Store original file  
        original_dir = 'data/original'  
        os.makedirs(original_dir, exist_ok=True)  
        original_path = os.path.join(original_dir, f"{checksum}.pdf")  
        os.link(file_path, original_path)  # Hard link (no duplication)  

        # Insert into database  
        metadata = extract_pdf_metadata(file_path)  
        cursor.execute('''  
            INSERT INTO files (file_path, file_type, checksum, metadata, original_path)  
            VALUES (?, ?, ?, ?, ?)  
        ''', (file_path, 'pdf', checksum, json.dumps(metadata), original_path))  

        conn.commit()  
        print(f"Ingested: {file_path}")  

    except Exception as e:  
        log_error(file_path, e)  
        print(f"FAILED: {file_path}")  
    finally:  
        conn.close()  

if __name__ == '__main__':  
    import sys  
    if len(sys.argv) != 2:  
        print("Usage: python ingest_pdf.py <path/to/file.pdf>")  
        sys.exit(1)  
    ingest_pdf(sys.argv[1])  