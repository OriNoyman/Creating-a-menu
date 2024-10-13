from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship, sessionmaker 

DATABASE_URL = DATABASE_URL = 'mssql+pyodbc://sa:OriDbMenu123@localhost:1433/TableDefinition?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Menu(Base):
    __tablename__ = 'Menu'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    parent_menu = relationship('Menu', remote_side=[id], back_populates='submenus', cascade="all, delete-orphan")
    submenus = relationship('Menu', back_populates='parent_menu', cascade="all, delete-orphan")

    items = relationship('MenuItem', back_populates='menu')
    options = relationship('MenuOption', back_populates='menu')
    users = relationship('User', secondary='user_menu', back_populates='menus')
    

class MenuItem(Base):
    __tablename__ = 'MenuItem'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    menu_id = Column(Integer, ForeignKey('Menu.id'))  
    menu = relationship('Menu', back_populates='items')
    action_route = Column(String)

class MenuOption(Base):
    __tablename__ = 'MenuOption'
    
    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('Menu.id'))
    action_id = Column(Integer, ForeignKey('MenuAction.id'))
    
    menu = relationship('Menu', back_populates='options')
    action = relationship('MenuAction', back_populates='MenuOptions')

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    
    menus = relationship('Menu', secondary='user_menu', back_populates='users')

user_menu_association = Table(
    'user_menu', Base.metadata,
    Column('user_id', Integer, ForeignKey('User.id')),
    Column('menu_id', Integer, ForeignKey('Menu.id'))
)

class MenuAction(Base):
    __tablename__ = 'MenuAction'

    id = Column(Integer, primary_key=True)
    action_name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    
    menu_options = relationship('MenuOption', back_populates='action')
    menus = relationship("Menu", secondary='menu_action_link', back_populates="actions")

    
menu_action_link = Table(
    'menu_action_link', Base.metadata,
    Column('menu_id', Integer, ForeignKey('Menu.id')),
    Column('menu_action_id', Integer, ForeignKey('MenuAction.id'))
)

Base.metadata.create_all(bind=engine)
