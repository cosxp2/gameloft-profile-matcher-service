from fastapi import APIRouter, HTTPException, Depends
from app.use_cases.match_player_profile import MatchPlayerProfileUseCase
from app.domain.exceptions import PlayerNotFoundError  
from app.adapters.dependencies import get_match_player_use_case

router = APIRouter()

@router.get("/get_client_config/{player_id}")
def get_client_config(player_id: str, use_case: MatchPlayerProfileUseCase = Depends(get_match_player_use_case)):
    try:
        profile = use_case.execute(player_id)
        return profile.model_dump()  
    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")