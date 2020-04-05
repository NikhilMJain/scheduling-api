from typing import List

from fastapi import Depends, APIRouter
from starlette.responses import Response

from src.app.api.managers.meeting_manager import MeetingManager
from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.config import API_PREFIX
from src.app.api.v1.models import User, UserResponse, MeetingPayload

router = APIRouter()


@router.post('/', status_code=201)
async def schedule_new_meeting(meeting: MeetingPayload, response: Response,
                               current_user: User = Depends(get_auth_user)):
    meeting_id = await MeetingManager().schedule_new_meeting(meeting=meeting, current_user=current_user)
    response.headers['Location'] = '{prefix}/meetings/{meeting_id}'.format(prefix=API_PREFIX, meeting_id=meeting_id)
    return {'meeting_id': meeting_id}


@router.get('/', response_model=List[UserResponse])
async def get_created_meetings( current_user: User = Depends(get_auth_user)):
    return await MeetingManager().get_created_meetings(current_user=current_user)
