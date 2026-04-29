import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from llm_discovery.core.config import settings

# set up HTTP Basic authentication
security = HTTPBasic()

# define a function to verify the provided credentials (username and password)
# ... to protect the API endpoints
def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, settings.AUTH_USERNAME)
    is_pass_ok = secrets.compare_digest(credentials.password, settings.AUTH_PASSWORD)
    
    # if either the username or password is incorrect, raise an HTTP 401 Unauthorized error
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username