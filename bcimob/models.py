# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, relation, sessionmaker
from sqlalchemy import create_engine


DBSession = scoped_session(sessionmaker(autoflush=False))

logger = logging.getLogger(__name__)


class classproperty(object):

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class ORMClass(object):
    """Base class for all models"""

    @classproperty
    def query(cls):
        """Return query object"""
        return DBSession.query(cls)

    @classmethod
    def get(cls, id):
        """Return one object given its primary key"""
        return DBSession.query(cls).get(id)


Base = declarative_base(cls=ORMClass)


class Player(Base):

    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    player_mame = Column(String(len('Player 1')), index=1)


def initialisedb():
    engine = create_engine('sqlite:///banco_imobiliario.db')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
