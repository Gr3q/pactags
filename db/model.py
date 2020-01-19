# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Package(Base):
    __tablename__ = 'Packages'

    name_id = Column(Text, primary_key=True)
    nice_name = Column(Text)
    repository = Column(Text)


class Tag(Base):
    __tablename__ = 'Tags'

    name_id = Column(Text, primary_key=True)
    nice_name = Column(Text)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class PackagesTag(Base):
    __tablename__ = 'Packages_Tags'

    id = Column(Integer, primary_key=True)
    package_id = Column(ForeignKey('Packages.name_id'))
    tag_id = Column(ForeignKey('Tags.name_id'))

    package = relationship('Package')
    tag = relationship('Tag')
