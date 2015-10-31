# -*- coding: utf-8 -*-

import logging
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship, sessionmaker, backref
from sqlalchemy import create_engine
from decimal import Decimal
import sqlalchemy.types as types

DBSession = scoped_session(sessionmaker(autoflush=False))
logging.basicConfig(
    filename='bcimob_db.log',
    format='%(asctime)s [%(levelname)s] %(name)s [%(process)d]: %(message)s',
)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class SqliteNumeric(types.TypeDecorator):
    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Decimal(value)

Numeric = SqliteNumeric


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
engine = create_engine('sqlite:///banco_imobiliario.db')
DBSession.configure(bind=engine)


class Player(Base):

    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    player_name = Column(String(len('Player 1')), index=1)
    balance = Column(Numeric(19, 10), nullable=True, default=float(25000.00))

    def update_balance(self, operation_type, amount):
        if operation_type == '1':  # Adição
            self.balance = float(self.balance) + amount
        elif operation_type == '2':  # Subtração
            self.balance = float(self.balance) - amount


class Movement(Base):

    __tablename__ = 'movement'
    __mapper_args__ = {'polymorphic_identity': 'movement'}

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(19, 10), nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False, index=True)
    player = relationship("Player", backref=backref('movement', lazy='dynamic'), foreign_keys=[player_id])
    move_type = Column(String(1), index=True)

    TYPES = {
        "IN": "1",
        "OUT": "2"
    }

    REV_TYPES = {
        "1": "IN",
        "2": "OUT"
    }

    VERBOSE_TYPES = {
        "IN": "Entrada",
        "OUT": "Saída"
    }

    @property
    def verbose_type(self):
        """Return a friendly name for the Movement state
           :return: str
        """

        return self.VERBOSE_TYPES[self.move_type]


def initialisedb():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
