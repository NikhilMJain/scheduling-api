import os

from databases import Database
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine, ForeignKey, Boolean, Date, \
    UniqueConstraint

from src.app.api.v1 import config

DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL)

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('token', String(100), nullable=False),
    Column('email', String(100), nullable=False),
    Column('first_name', String(100), nullable=False),
    Column('last_name', String(100), nullable=False),
    UniqueConstraint('email')
)

slots = Table(
    'slots',
    metadata,
    Column('slot_id', Integer, primary_key=True),
    Column('date', Date, nullable=False),
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('start_time', DateTime, nullable=False),
    Column('is_available', Boolean, nullable=False),
    UniqueConstraint('user_id', 'start_time')
)


meetings = Table(
    'meetings',
    metadata,
    Column('meeting_id', Integer, primary_key=True),
    Column('slot_id', Integer, ForeignKey('slots.slot_id'), nullable=False),
    Column('creator_id', ForeignKey('users.user_id'), nullable=False),
    Column('status', String(50), nullable=False),
    UniqueConstraint('slot_id', 'creator_id')
)


meeting_guests = Table(
    'meeting_guests',
    metadata,
    Column('meeting_guest_id', Integer, primary_key=True),
    Column('meeting_id', Integer, ForeignKey('meetings.meeting_id'), nullable=False),
    Column('email', String(50), nullable=False),
    UniqueConstraint('meeting_id', 'email')
)


database = Database(DATABASE_URL)
