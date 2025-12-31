from sqlalchemy import create_engine
from app.db.base import Base

# Import the models package to ensure model modules are loaded
# which registers all models with SQLAlchemy metadata via app.models.__init__
from app import models  # noqa: F401

import os
from dotenv import load_dotenv

def init_db():
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment or use default SQLite
    database_url = os.getenv("DATABASE_URL", "sqlite:///./followwise.db")
    
    # Create engine and tables
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    
    print(f"Creating database tables at: {database_url}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
