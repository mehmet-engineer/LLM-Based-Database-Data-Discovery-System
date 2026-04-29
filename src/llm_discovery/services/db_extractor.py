import psycopg2

def extract_schema_from_db(host, port, database, username, password):
    # establish connection to the database to extract schema information
    connection = psycopg2.connect(host=host, port=port, dbname=database, user=username, password=password)
    cursor = connection.cursor()
    
    # store schema information in a dictionary
    schema_data = {}
    
    # Get all tables in database
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Get columns for each table
    for table in tables:
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table,))
        schema_data[table] = [{"name": row[0], "type": row[1]} for row in cursor.fetchall()]
        
    cursor.close()
    connection.close()
    return schema_data

def get_column_samples(host, port, database, username, password, table_name, column_name, limit):
    # establish connection to the database to extract sample data from specific table and column
    connection = psycopg2.connect(host=host, port=port, dbname=database, user=username, password=password)
    cursor = connection.cursor()
    
    # fetch sample data for the specified column
    query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL LIMIT %s"
    cursor.execute(query, (limit,))
    samples = [str(row[0]) for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    return samples