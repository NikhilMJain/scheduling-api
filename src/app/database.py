import os

from databases import Database
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine, ForeignKey, Boolean, Date

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(50), nullable=False),
    Column('token', String(100), nullable=False),
    Column('email', String(100), nullable=False)
)

slots = Table(
    'slots',
    metadata,
    Column('slot_id', Integer, primary_key=True),
    Column('date', Date, nullable=False),
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False),
    Column('start_time', DateTime, nullable=False),
    Column('is_available', Boolean, nullable=False)
)


meetings = Table(
    'meetings',
    metadata,
    Column('meeting_id', Integer, primary_key=True),
    Column('slot_id', Integer, ForeignKey('slots.slot_id'), nullable=False),
    Column('setter_email', String(50), nullable=False),
    Column('status', String(50), nullable=False)
)


meeting_members = Table(
    'meeting_members',
    metadata,
    Column('meeting_member_id', Integer, primary_key=True),
    Column('meeting_id', Integer, ForeignKey('meetings.meeting_id'), nullable=False),
    Column('email', String(50), nullable=False),
    Column('role', String(50), nullable=True)
)


database = Database(DATABASE_URL)
