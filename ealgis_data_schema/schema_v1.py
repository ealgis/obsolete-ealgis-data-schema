from sqlalchemy.schema import (
    Table,
    Column,
    MetaData,
    ForeignKey)
from sqlalchemy.types import (
    Text,
    JSON,
    DateTime,
    Integer,
    String)
from collections import defaultdict
import datetime


class SchemaStore:
    def __init__(self):
        self.metadata = defaultdict(MetaData)
        self.tables = defaultdict(list)

    def _import_schema(self, schema_name):
        def fkey(target):
            return ForeignKey(schema_name + '.' + target)

        metadata = self.metadata[schema_name]
        tables = self.tables[schema_name]
        tables.append(Table(
            "ealgis_metadata", metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(256)),
            Column('version', String(256)),
            Column('description', Text()),
            Column('date_created', DateTime(timezone=True), default=datetime.datetime.utcnow),
            schema=schema_name))
        tables.append(Table(
            "table_info", metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(256)),
            Column('metadata', JSON()),
            schema=schema_name))
        tables.append(Table(
            "column_info", metadata,
            Column('id', Integer, primary_key=True),
            Column('table_info_id', Integer, fkey('table_info.id'), nullable=False),
            Column('name', String(256)),
            Column('metadata', JSON()),
            schema=schema_name))
        tables.append(Table(
            "geometry_source", metadata,
            Column('id', Integer, primary_key=True),
            Column('gid', String(256)),
            Column('table_info_id', Integer, fkey('table_info.id'), nullable=False),
            Column('geometry_type', String(256)),
            schema=schema_name))
        tables.append(Table(
            "geometry_source_column", metadata,
            Column('id', Integer, primary_key=True),
            Column('geometry_source_id', Integer, fkey('geometry_source.id'), nullable=False),
            Column('column', String(256)),
            Column('srid', Integer),
            schema=schema_name))
        tables.append(Table(
            "geometry_linkage", metadata,
            Column('id', Integer, primary_key=True),
            Column('table_info_id', Integer, fkey('table_info.id'), nullable=False),
            Column('geometry_source_id', Integer, fkey('geometry_source.id'), nullable=False),
            Column('geo_column', String(256)),
            Column('attr_column', String(256)),
            schema=schema_name))
        tables.append(Table(
            "mailbox", metadata,
            Column('id', Integer, primary_key=True),
            Column('from', String(256)),
            Column('to', String(256)),
            Column('message', JSON()),
            schema=schema_name))

    def load_schema(self, schema_name):
        if schema_name not in self.metadata:
            self._import_schema(schema_name)
        return self.metadata[schema_name], self.tables[schema_name]


store = SchemaStore()
