from fastapi import FastAPI
from llm_discovery.database import engine, Base
from llm_discovery.routers import auth, metadata, classification

# initialize database tables
Base.metadata.create_all(bind=engine)

# initialize FastAPI app with title
title = "LLM Database Discovery API"
app = FastAPI(title=title)

# register routers
app.include_router(auth.router)
app.include_router(metadata.router)
app.include_router(classification.router)