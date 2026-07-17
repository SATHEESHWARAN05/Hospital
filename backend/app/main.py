from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import hospitals, doctors, rooms, bookings

# Create all tables on startup (for development convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Front Desk API",
    version="1.0.0",
    description="Simple hospital listing, search, doctor/room availability, and booking API.",
)

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(hospitals.router, prefix="/api", tags=["Hospitals"])
app.include_router(doctors.router, prefix="/api", tags=["Doctors"])
app.include_router(rooms.router, prefix="/api", tags=["Rooms"])
app.include_router(bookings.router, prefix="/api", tags=["Bookings"])


@app.get("/")
def root():
    return {"message": "Hospital Front Desk API is running"}
