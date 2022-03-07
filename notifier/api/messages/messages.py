from fastapi import APIRouter, Depends

from ..users.utils import get_user_id
from ..utils.sender import send_mess
from .handlers import mess_handler
from .schemas import Confirmation, Delay, Invite, Registration

router = APIRouter()


@router.post('/registration')
async def tournament_reg(reg: Registration,
                         client_id: str = Depends(get_user_id)):
    """
    Get messages of service x, for realtime sending, after user
    registration on tournament.
    """
    return await mess_handler(client_id, reg.message)


@router.post('/reg_confirm')
async def tournament_confirm(conf: Confirmation,
                             client_id: str = Depends(get_user_id)):
    """
    Get messages of service y, for delay sending (1 hour before tournament).
    """
    return await mess_handler(client_id, conf.message, conf.date)


@router.post('/tourn_invite')
async def tourn_invite(inv: Invite, client_id: str = Depends(get_user_id)):
    """
    Get messages of service z, for delay sending (on tournament begin).
    """
    return await mess_handler(client_id, inv.message, inv.date)


@router.post('/delay')
async def delay(mess: Delay):
    """Send delayed messages."""
    return await send_mess(mess.client_id, mess.message, mess.date)
