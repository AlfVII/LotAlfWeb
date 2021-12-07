import pandas
import sqlalchemy
from sqlalchemy.ext.automap import automap_base


class CommentsDB():
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        engine = sqlalchemy.create_engine("postgresql://alfvii:2Galletas!@localhost:5432/autop", connect_args={'connect_timeout': 10})
        schema = "public"

        metadata = sqlalchemy.MetaData()
        metadata.reflect(engine, schema=schema, only=['comments'])
        Base = automap_base(metadata=metadata)
        Base.prepare()
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
