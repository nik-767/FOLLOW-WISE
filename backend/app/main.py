from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Import routers (using the correct path)
from app.api.endpoints import auth, leads, users, sent_emails


# Load environment variables
load_dotenv()

# 1. CREATE THE APP (Just Once!)
app = FastAPI(
    title="FollowWise API",
    description="AI sales follow-up automation tool",
    version="0.1.0"
)

# 2. ADD CORS MIDDLEWARE (Immediately after creating app)
origins = [
    "http://localhost:3000", # Frontend (Port 3000)
    "http://localhost:3001", # Frontend (Port 3001) - Vite default
    "http://localhost:3002", # Frontend (Port 3002)
    "http://localhost:5173", # Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Use the list above
    allow_credentials=True,    # Allow cookies/headers
    allow_methods=["*"],       # Allow all methods (POST, GET, etc)
    allow_headers=["*"],       # Allow all headers
)

# 3. CONFIGURE ROUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(sent_emails.router, prefix="/api/sent-emails", tags=["sent-emails"])

@app.get("/")
async def root():
    return {"message": "Welcome to FollowWise API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}