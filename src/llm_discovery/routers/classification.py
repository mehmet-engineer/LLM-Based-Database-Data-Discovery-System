from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from llm_discovery.database import get_db
from llm_discovery.schemas import ClassifyRequest
from llm_discovery.models import ColumnRecord
from llm_discovery.core.security import verify_credentials
from llm_discovery.services.db_extractor import get_column_samples
from llm_discovery.services.llm_service import classify_samples_with_llm

# create a router for classification endpoints
router = APIRouter(prefix="/classify", tags=["Classification"], dependencies=[Depends(verify_credentials)])

# handling POST /classify
@router.post("")
def classify_data(request: ClassifyRequest, db: Session = Depends(get_db)):
    # fetch the column record from the database
    col_record = db.query(ColumnRecord).filter(ColumnRecord.id == request.column_id).first()
    if not col_record:
        raise HTTPException(status_code=404, detail="Column not found")
        
    table_record = col_record.table
    metadata_record = table_record.metadata_record
    
    # fetch sample data for the specified column
    try:
        samples = get_column_samples(
            metadata_record.host, metadata_record.port, metadata_record.database_name,
            metadata_record.username, metadata_record.encrypted_password,
            table_record.table_name, col_record.column_name, request.sample_count
        )
        
        if not samples:
            return {"message": "No sample data found to classify."}
        
        # classify the samples using the LLM service to get classification probabilities
        distribution = classify_samples_with_llm(col_record.column_name, samples)
        
        return {"column_id": request.column_id, "classification_probabilities": distribution}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))