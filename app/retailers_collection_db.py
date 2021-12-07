import pandas
import sqlalchemy
from sqlalchemy.ext.automap import automap_base


class RetailersCollectionDB():
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        engine = sqlalchemy.create_engine("postgresql://alfvii:2Galletas!@localhost:5432/autop", connect_args={'connect_timeout': 10})
        schema = "public"

        metadata = sqlalchemy.MetaData()
        metadata.reflect(engine, schema=schema, only=['retailers_collection'])
        Base = automap_base(metadata=metadata)
        Base.prepare()
        self.RetailersCollectionTable = Base.classes.retailers_collection

        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()

    def get_all_retailers(self):
        query = self.session.query(self.RetailersCollectionTable)
        data = pandas.read_sql(query.statement, query.session.bind)
        return data

    def get_retailers(self, fields, values):
        query = self.session.query(self.RetailersCollectionTable)
        for index in range(0, len(fields)):
            query = query.filter(getattr(self.RetailersCollectionTable, fields[index]) == values[index])
        data = pandas.read_sql(query.statement, query.session.bind)
        return data

    def get_retailers_like(self, fields, values):
        query = self.session.query(self.RetailersCollectionTable)
        for index in range(0, len(fields)):
            query = query.filter(getattr(self.RetailersCollectionTable, fields[index]).like(values[index]))
        data = pandas.read_sql(query.statement, query.session.bind)
        return data

    def update_retailer(self, data):
        query = self.session.query(self.RetailersCollectionTable).filter(self.RetailersCollectionTable.retailer_region == data['retailer_region'])
        query = query.filter(self.RetailersCollectionTable.retailer_province == data['retailer_province'])
        query = query.filter(self.RetailersCollectionTable.retailer_town == data['retailer_town'])
        query = query.filter(self.RetailersCollectionTable.retailer_number == data['retailer_number'])
        existing_data = pandas.read_sql(query.statement, query.session.bind)

        if existing_data.empty:
            self.session.add(self.RetailersCollectionTable(**data))
        else:
            query = query.update(data)
        self.session.commit()

    def delete_retailer(self, data):
        query = self.session.query(self.RetailersCollectionTable).filter(self.RetailersCollectionTable.retailer_region == data['retailer_region'])
        query = query.filter(self.RetailersCollectionTable.retailer_province == data['retailer_province'])
        query = query.filter(self.RetailersCollectionTable.retailer_town == data['retailer_town'])
        query = query.filter(self.RetailersCollectionTable.retailer_number == data['retailer_number'])
        existing_data = pandas.read_sql(query.statement, query.session.bind)

        if not existing_data.empty:
            query = query.delete()
        self.session.commit()

    def close_connection(self):
        self.session.close()
