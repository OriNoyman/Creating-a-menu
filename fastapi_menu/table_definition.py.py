from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menus'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    options = relationship('MenuOption', back_populates='menu')
    
    parent_menu = relationship('Menu', remote_side=[id], back_populates='submenus', cascade="all, delete-orphan")
    submenus = relationship('Menu', back_populates='parent_menu', cascade="all, delete-orphan")
    items = relationship('MenuItem', back_populates='menu')

    users = relationship('User', secondary='user_menu', back_populates='menus')
    actions = relationship('MenuAction', secondary="menu_to_action", back_populates='menus')

class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    menu_id = Column(Integer, ForeignKey('menus.id'))  
    menu = relationship('Menu', back_populates='items')

class MenuOption(Base):
    __tablename__ = 'menu_options'
    
    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    action_id = Column(Integer, ForeignKey('menu_action.id'))
    
    menu = relationship('Menu', back_populates='options')
    action = relationship('MenuAction', back_populates='menu_options')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
    menus = relationship('Menu', secondary='user_menu', back_populates='users')

user_menu_association = Table(
    'user_menu', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('menu_id', Integer, ForeignKey('menus.id'))
)

class MenuAction(Base):
    __tablename__ = 'menu_action'

    id = Column(Integer, primary_key=True)
    action_name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    
    menu_options = relationship('MenuOption', back_populates='action')
    menus = relationship("Menu", secondary='menu_action_link', back_populates="actions")

    
menu_action_link = Table(
    'menu_action_link', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id')),
    Column('menu_action_id', Integer, ForeignKey('menu_action.id'))
)
