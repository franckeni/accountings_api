from fastapi import APIRouter

from .create_router import create_router
from .delete_router import delete_router
from .find_all_router import find_all_router
from .find_one_router import find_one_router
from .update_router import update_router

router = APIRouter(tags=["Accounts Type"])

router.include_router(find_all_router)
router.include_router(find_one_router)
router.include_router(create_router)
router.include_router(update_router)
router.include_router(delete_router)
