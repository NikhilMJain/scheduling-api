from fastapi import Depends, APIRouter
from starlette.responses import Response

from src.app.api.managers.user_manager import UserManager
from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.config import API_PREFIX
from src.app.api.v1.models import UserResponse, User, NewUser
from src.app.logger import log

router = APIRouter()


@router.get('/{user_id}', response_model=UserResponse)
async def get_users(user_id: int = None, current_user: User = Depends(get_auth_user)):
    return await UserManager().get_user_by_id(user_id)


@router.post('/', status_code=201)
async def add_new_user(user: NewUser, response: Response):
    log.info('Adding new user {}'.format(user))
    new_user = await UserManager().add_user(user=user)
    response.headers['Location'] = '{prefix}/users/{user_id}'.format(prefix=API_PREFIX, user_id=new_user['user_id'])
    return new_user
