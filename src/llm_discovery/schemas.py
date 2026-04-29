from pydantic import BaseModel

# ////////////////////////////////////////////////////////////////////////
# Pydantic is used to to handle type issues, request validation
# ... and define request models for request parsing in FastAPI endpoints.
# ////////////////////////////////////////////////////////////////////////

# Pydantic DBConnectionRequest model
class DBConnectionRequest(BaseModel):
    host: str
    port: str
    database: str
    username: str
    password: str

# Pydantic ClassifyRequest model
class ClassifyRequest(BaseModel):
    column_id: str
    sample_count: int = 10