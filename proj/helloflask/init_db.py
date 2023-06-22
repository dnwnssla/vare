from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib
# Declare connection
password = urllib.parse.quote("It12345!")
mysql_url = f'mysql://root:{password}@vare.c3qqjfoelna8.ap-northeast-2.rds.amazonaws.com:3306/project?charset=utf8'
engine = create_engine(mysql_url, echo=True)

# Declare & create Session
db_session = scoped_session( sessionmaker(autocommit=False, autoflush=False, bind=engine) )

# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
    Base.metadata.create_all(bind=engine)
