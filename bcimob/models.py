# -*- coding: utf-8 -*-

import logging
import warnings
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship, sessionmaker, backref
from sqlalchemy import create_engine
from sqlalchemy.exc import SAWarning
import money

DBSession = scoped_session(sessionmaker(autoflush=False))

logger = logging.getLogger(__name__)

warnings.filterwarnings(
    'ignore',
    r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
    "and SQLAlchemy must convert from floating point - rounding errors and other "
    "issues may occur\. Please consider storing Decimal numbers as strings or "
    "integers on this platform for lossless storage\.$",
    SAWarning, r'^sqlalchemy\.sql\.type_api$')


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
    amount = Column(Numeric(19, 10, asdecimal=True), nullable=False)
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
