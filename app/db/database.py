from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Tokens table
class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mint_address = Column(String, unique=True, nullable=False)
    symbol = Column(String, nullable=False)
    decimals = Column(Integer, nullable=False)

# Pools table
class Pool(Base):
    __tablename__ = 'pools'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_address = Column(String, unique=True, nullable=False)
    token_a = Column(String, ForeignKey('tokens.mint_address'))
    token_b = Column(String, ForeignKey('tokens.mint_address'))
    platform = Column(String, nullable=False)  # e.g., Raydium, Jupiter
    fee = Column(Float, nullable=True)

# Prices table
class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(Integer, ForeignKey('tokens.id'))
    pool_id = Column(Integer, ForeignKey('pools.id'))
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Trades table
class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_a = Column(String, ForeignKey('tokens.mint_address'))
    token_b = Column(String, ForeignKey('tokens.mint_address'))
    amount_in = Column(Float, nullable=False)
    amount_out = Column(Float, nullable=False)
    pool_id = Column(Integer, ForeignKey('pools.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

# Arbitrage opportunities
class ArbitrageOpportunity(Base):
    __tablename__ = 'arbitrage_opportunities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_a = Column(String, ForeignKey('tokens.mint_address'))
    token_b = Column(String, ForeignKey('tokens.mint_address'))
    profit = Column(Float, nullable=False)
    pool_a = Column(Integer, ForeignKey('pools.id'))
    pool_b = Column(Integer, ForeignKey('pools.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

# Initialize DB
DATABASE_URL = "postgresql://user:password@localhost:5432/solana_arbitrage"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
