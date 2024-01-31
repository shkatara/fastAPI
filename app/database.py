from sqlalchemy import Column, String,Integer,Table,MetaData,create_engine,Select


#create engine for sqlalchemy
engine = create_engine("mysql+pymysql://root:redhat123@localhost/posts")

#create connection to mysql
conn = engine.connect()

#meta object to hold table metadata
posts_table_meta = MetaData()
users_table_meta = MetaData()


#define table structure
posts_table = Table('posts',posts_table_meta,Column('id', Integer, primary_key=True, autoincrement=True),Column('title', String(255)),Column('firstname', String(255)),Column('lastname', String(255)),Column('content',String(255)))
users_table = Table('users',users_table_meta,Column('email', String(255), primary_key=True),Column('password', String(255)),Column('pwhash', String(255)))

posts_table_meta.create_all(engine)
users_table_meta.create_all(engine)
