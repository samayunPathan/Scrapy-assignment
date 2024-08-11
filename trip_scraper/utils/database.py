# # trip_scraper/utils/database.py

# import psycopg2
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from trip_scraper.models.hotel import Base
# from sqlalchemy import create_engine

# DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/scrap_data'

# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)


# def create_database_if_not_exists():
#     """Create the database if it does not exist."""
#     # Connection parameters for the PostgreSQL server
#     conn_str = 'dbname=postgres user=postgres password=1234 host=localhost port=5432'
#     conn = psycopg2.connect(conn_str)
#     conn.autocommit = True  # Required to run CREATE DATABASE command

#     cursor = conn.cursor()
#     try:
#         cursor.execute('CREATE DATABASE scrap_data')
#         print("Database created successfully!")
#     except psycopg2.errors.DuplicateDatabase:
#         print("Database already exists.")
#     finally:
#         cursor.close()
#         conn.close()

# # Call this function to create the database if it does not exist
# create_database_if_not_exists()

# # Create an engine and bind it to the database
# engine = create_engine(DATABASE_URL, echo=True)

# # Create all tables
# Base.metadata.create_all(engine)

# # Create a session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db_session():
#     """Create and return a new database session."""
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()

# def create_tables():
#     """Create all tables in the database."""
#     Base.metadata.create_all(bind=engine)

# def close_db_session(session):
#     """Close the database session."""
#     session.close()



# def get_db_session():
#     # Create a session and return it directly
#     session = Session()
#     return session

# def close_db_session(session):
#     # Close the session properly
#     session.close()
