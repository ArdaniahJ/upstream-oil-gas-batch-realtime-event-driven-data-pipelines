import pandas as pd
import os
from openpyxl import load_workbook
from sqlalchemy import create_engine
import urllib
import pyodbc
from config import PSC_CONTRACT, EXCEL_COLUMNS_AVAILABILITY, EXCEL_COLUMNS_ACTIVITY


# --------------------- ETL (EXTRACTION) -------------------





# --------------------- ARCHIVE -------------------
def archive_file(file_path):
    # Move the file to the archive folder
    archive_folder = os.path.join(ARCHIVE_FOLDER, os.path.basename(file_path))
    move(file_path, archive_folder)

if __name__ == "__main__":
    monitor_uploads_folder()
