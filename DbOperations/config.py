from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from RetryingQuery import RetryingQuery

SQLALCHEMY_DATABASE_URI = 'mysql://scraping:scraping@database-1.cyfzarjmgkc6.eu-north-1.rds.amazonaws.com:3306/scraping'

engine = create_engine(SQLALCHEMY_DATABASE_URI,pool_size=5,
                                      max_overflow=10,
                                      pool_recycle=300,
                                      pool_pre_ping=True,
                                      pool_use_lifo=True)
engine.connect()
print("after connect to DB:" + SQLALCHEMY_DATABASE_URI)

print("before session:" + SQLALCHEMY_DATABASE_URI)

session = sessionmaker(bind=engine, autoflush=True,  query_cls=RetryingQuery)
Session = session()