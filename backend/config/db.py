from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:mysql6201@localhost:3306/users_db")
#conn = engine.connect()
meta_data = MetaData()
