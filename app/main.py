from fastapi import FastAPI
from app.adapters.fast_api.profile import router as profile_router

app = FastAPI(
    title="Profile Matcher Service",
    version="1.0.0",
    description="Matches player profiles against active campaigns"
)

app.include_router(profile_router)