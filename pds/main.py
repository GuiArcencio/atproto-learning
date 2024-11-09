from storage.sqlite.engine import setup_connection
from storage.sqlite.models import Base

engine = setup_connection()

Base.metadata.create_all(engine)