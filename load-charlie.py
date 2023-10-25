#------------INSERT/LOAD DATA TO DATABSE ----------------------

import urllib.parse
from sqlalchemy import create_engine

# Database connection params
DB_SERVER = "PTSG-1AVEVADB01"
DB_NAME = "USDP_AGNES"
DB_USERNAME = "AGNES_USERNAME"
DB_PASSWORD = "@gn3s23"

#----------------------------------------------------------------------------------------------------

def load_data_into_database(data, category_name, db_server, db_name, db_username, db_password):
    """
    Load data into the database based on the specified category (Supply or Demand)

    Args:
        data(dict): A dictionary containing data fields to be loaded into the database
        category_name (str): The category name ("Supply" or "Demand")
        db_server (str): The SQL Server's hostname.
        db_name (str): The database name.
        db_username (str): The database username.
        db_password (str): The database password.

    Raises:
        ValueError: If an invalid category name is provided.
    
    Note:
        - The 'data' params should contain keys for "OPERATOR_NAME", "LOCATION_NAME", "DATE", and "VALUE".
        - The database connection is created using SQLAlchemy.

    Returns:
        None
    """

    # Create a connetion to MSSQL Server
    params = urllib.parse.quote_plus(f"DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}")
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    # Define the SQL INSERT STATEMENT to insert data into SUPPLY/DEMAND tables
    sql_demand = "INSERT INTO dbo.AVAILABILITY_DEMAND (CUSTOMER_ID, MODULE_ID, REPORTING_DATE, VALUE, CREATED_BY, CREATED_DATE, MODIFIED_BY, MODIFIED_DATE) VALUES (:CUSTOMER_ID, :MODULE_ID, :REPORTING_DATE, :VALUE, :CREATED_BY, :CREATED_DATE, :MODIFIED_BY, :MODIFIED_DATE)"
    sql_supply = "INSERT INTO dbo.AVAILABILITY_SUPPLY (PA_CONTRACTOR_ID, FIELD_ID, REPORTING_DATE, VALUE, CREATED_BY, CREATED_DATE, MODIFIED_BY, MODIFIED_DATE) VALUES (:PA_CONTRACTOR_ID, :FIELD_ID, :REPORTING_DATE, :VALUE, :CREATED_BY, :CREATED_DATE, :MODIFIED_BY, :MODIFIED_DATE)"

    # Map the input data to its fields (fields = columns, records = rows)
    field_mapping_demand = {
        "CUSTOMER_ID": data["OPERATOR_NAME"],
        "MODULE_ID": data["LOCATION_NAME"],
        "REPORTING_DATE": data["DATE"],
        "VALUE": data["VALUE"]
    }

    field_mapping_supply = {
        "PA_CONTRACTOR_ID": data["OPERATOR_NAME"],
        "FIELD_ID": data["LOCATION_NAME"],
        "REPORTING_DATE": data["DATE"],
        "VALUE": data["VALUE"]
    }

    # Determine the SQL statement based on the category
    if category_name == "Supply":
        sql_statement = sql_supply
        field_mapping = field_mapping_supply
    elif category_name == "Demand":
        sql_statement = sql_demand
        field_mapping = field_mapping_demand
    else:
        raise ValueError("Invalid category name.")
    
    # Manage the connection with the database (conn.execute will run based on the category_name)
    # (**) is used to unpack the dict items into the SQL statement
    with engine.connect() as conn:
        conn.execute(sql_demand, **field_mapping)