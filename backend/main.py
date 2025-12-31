"""
Compatibility shim for ASGI servers.

Some developers run `uvicorn main:app` from the `backend/` folder.
The real FastAPI app lives at `app.main:app`. This file re-exports
the app so either import style works.

Generated automatically by QA assistant to fix "Could not import module 'main'".
"""
from app.main import app  # re-export FastAPI instance
