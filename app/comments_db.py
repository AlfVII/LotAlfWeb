import pandas
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
import os


class CommentsDB():
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        engine = sqlalchemy.create_engine(f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_ADDRESS']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}", connect_args={'connect_timeout': 10})
        schema = "public"

        metadata = sqlalchemy.MetaData()
        metadata.reflect(engine, schema=schema)
        # metadata.reflect(engine, schema=schema, only=['comments'])
        print(metadata.tables.keys())
        Base = automap_base(metadata=metadata)
        Base.prepare()
        print(dir(Base.classes))
        self.CommentsTable = Base.classes.comments

        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()

    def get_all_comments(self):
        query = self.session.query(self.CommentsTable)
        hundred_data = pandas.read_sql(query.statement, query.session.bind)
        return hundred_data

    def insert_comment(self, name, email, comment):

        self.session.add(self.CommentsTable(
            name=name,
            email=email,
            comment=comment
        ))
        self.session.commit()

    def close_connection(self):
        self.session.close()
