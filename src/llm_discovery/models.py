import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from llm_discovery.database import Base

# ////////////////////////////////////////////////
# SQLAlchemy ORM model for Metadata records
class MetadataRecord(Base):
    __tablename__ = "metadata_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    database_name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    port = Column(String, nullable=False)
    username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tables = relationship("TableRecord", back_populates="metadata_record", cascade="all, delete-orphan")

# ////////////////////////////////////////////////
# SQLAlchemy ORM model for Table records
class TableRecord(Base):
    __tablename__ = "table_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metadata_id = Column(String, ForeignKey("metadata_records.id"))
    table_name = Column(String, nullable=False)
    metadata_record = relationship("MetadataRecord", back_populates="tables")
    columns = relationship("ColumnRecord", back_populates="table", cascade="all, delete-orphan")

# ////////////////////////////////////////////////
# SQLAlchemy ORM model for Column records
class ColumnRecord(Base):
    __tablename__ = "column_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    table_id = Column(String, ForeignKey("table_records.id"))
    column_name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    table = relationship("TableRecord", back_populates="columns")