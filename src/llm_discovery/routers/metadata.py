from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from llm_discovery.database import get_db
from llm_discovery.schemas import DBConnectionRequest
from llm_discovery.models import MetadataRecord, TableRecord, ColumnRecord
from llm_discovery.core.security import verify_credentials
from llm_discovery.services.db_extractor import extract_schema_from_db

# create a router for metadata endpoints
router = APIRouter(prefix="", tags=["Metadata"], dependencies=[Depends(verify_credentials)])

# handling POST /db/metadata
@router.post("/db/metadata")
def create_metadata(request: DBConnectionRequest, db: Session = Depends(get_db)):
    try:
        # extract schema using the service
        schema_data = extract_schema_from_db(
            request.host, request.port, request.database, request.username, request.password
        )
        
        # save metadata as a record in the database
        metadata = MetadataRecord(
            database_name=request.database, host=request.host, port=request.port,
            username=request.username, encrypted_password=request.password
        )
        db.add(metadata)
        db.flush()
        
        # add tables and columns records with ORM models
        for table_name, columns in schema_data.items():
            table_record = TableRecord(metadata_id=metadata.id, table_name=table_name)
            db.add(table_record)
            db.flush()
            
            for col in columns:
                col_record = ColumnRecord(table_id=table_record.id, column_name=col["name"], data_type=col["type"])
                db.add(col_record)
                
        db.commit()
        return {"metadata_id": metadata.id, "status": "success"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# handling GET /metadata
@router.get("/metadata")
def list_metadata(db: Session = Depends(get_db)):
    # list all metadata records with basic info
    records = db.query(MetadataRecord).all()
    return [{"metadata_id": r.id, "database_name": r.database_name, "creation_date": r.created_at, "table_count": len(r.tables)} for r in records]

# handling GET /metadata/{metadata_id}
@router.get("/metadata/{metadata_id}")
def get_metadata(metadata_id: str, db: Session = Depends(get_db)):
    # get detailed metadata info including tables and columns
    record = db.query(MetadataRecord).filter(MetadataRecord.id == metadata_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    # create tables_list to return table and column details
    tables_list = []
    for table in record.tables:
        cols = [{"column_id": c.id, "column_name": c.column_name, "data_type": c.data_type} for c in table.columns]
        tables_list.append({"table_name": table.table_name, "columns": cols})
        
    return {"metadata_id": record.id, "tables": tables_list}

# handling DELETE /metadata/{metadata_id}
@router.delete("/metadata/{metadata_id}")
def delete_metadata(metadata_id: str, db: Session = Depends(get_db)):
    # delete the metadata record and all related tables and columns
    record = db.query(MetadataRecord).filter(MetadataRecord.id == metadata_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Metadata not found")
        
    db.delete(record)
    db.commit()
    
    return {"status": "deleted", "metadata_id": metadata_id}