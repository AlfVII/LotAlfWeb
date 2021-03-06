import pandas
import sqlalchemy
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql.expression import cast


class NumbersCollectionDB():
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        engine = sqlalchemy.create_engine(f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_ADDRESS']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}", connect_args={'connect_timeout': 10})
        schema = "public"

        metadata = sqlalchemy.MetaData()
        metadata.reflect(engine, schema=schema, only=['numbers_collection'])
        Base = automap_base(metadata=metadata)
        Base.prepare()
        self.NumbersCollectionTable = Base.classes.numbers_collection

        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()

    def get_filtered_numbers(self, filters, limit):
        query = self.session.query(self.NumbersCollectionTable.number)
        for filt in filters:
            if filt['filled'] == '0':
                query = query.filter(cast(getattr(self.NumbersCollectionTable, filt['name']), sqlalchemy.String).is_(None))
                # query = query.filter(cast(getattr(self.NumbersCollectionTable, filt['name']), sqlalchemy.String) != '')
            else:
                query = query.filter(cast(getattr(self.NumbersCollectionTable, filt['name']), sqlalchemy.String).like("%" + filt['value'] + "%"))

        query = query.order_by("number")
        if limit is not None:
            query = query.limit(limit)
        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        data = pandas.read_sql(query.statement, query.session.bind).sort_values(by='number', ascending=True)
        return data

    def get_all_numbers(self):
        query = self.session.query(self.NumbersCollectionTable)
        hundred_data = pandas.read_sql(query.statement, query.session.bind)
        return hundred_data

    def get_hundred(self, hundred):
        query = self.session.query(self.NumbersCollectionTable).filter(self.NumbersCollectionTable.number >= int(hundred))
        query = query.filter(self.NumbersCollectionTable.number < int(hundred) + 100).order_by("number")
        hundred_data = pandas.read_sql(query.statement, query.session.bind)
        return hundred_data

    def get_number(self, number):
        query = self.session.query(self.NumbersCollectionTable).filter(self.NumbersCollectionTable.number == int(number))
        hundred_data = pandas.read_sql(query.statement, query.session.bind)
        return hundred_data

    def update_number(self, number, data):
        self.session.query(self.NumbersCollectionTable).filter(self.NumbersCollectionTable.number == number).update(data)
        self.session.commit()

    def close_connection(self):
        self.session.close()
