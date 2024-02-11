from sqlalchemy import Column, String,Integer,Table,MetaData,create_engine,Select,ForeignKey
#from oauth2 import validate_access_token

#create engine for sqlalchemy
engine = create_engine("mysql+pymysql://root:redhat123@localhost/posts")

#create connection to mysql
conn = engine.connect()

#meta object to hold table metadata
posts_table_meta = MetaData()
users_table_meta = MetaData()


#define table structure
users_table = Table(
    'users',
    users_table_meta,
    Column('email', String(255), primary_key=True),
    Column('password', String(255)),
    Column('pass_salt', String(255))
)

posts_table = Table(
    'posts',
    posts_table_meta,
    Column('post_id', Integer, primary_key=True, autoincrement=True),
    Column('post_title', String(255)),
    Column('post_owner', String(255),ForeignKey(users_table.c.email)),
    Column('post_content',String(255))
)

users_table_meta.create_all(engine)
posts_table_meta.create_all(engine)

def find_post_in_db(post_id: str, email: str):
    #select_sql_instruction = Select(posts_table.c.post_title,posts_table.c.post_content,posts_table.c.post_owner).where(posts_table.c.id == post_id)
    select_sql_instruction = Select(posts_table.c.post_title,posts_table.c.post_content,posts_table.c.post_owner).where(posts_table.c.post_owner==email,posts_table.c.post_id == post_id).join(users_table)

    exec_sql = conn.execute(select_sql_instruction).fetchone()
    return list(exec_sql) if exec_sql is not None else  {"msg":"Post not found"}

def find_user_in_db(user_email):
    select_sql_where_instruction = Select("*").where(users_table.c.email == user_email)
    exec_sql = conn.execute(select_sql_where_instruction).fetchone()
    return list(exec_sql) if exec_sql is not None else  {"msg":"User not found"}