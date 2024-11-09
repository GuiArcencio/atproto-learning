from sqlalchemy import create_engine

def setup_connection():
    engine = create_engine("sqlite+pysqlite:///data.db")
    return engine