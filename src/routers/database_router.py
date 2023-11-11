import os
import shutil
import time
import zipfile

from fastapi import File, UploadFile, APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ml.preprocessing_data.Articles_path import get_path

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)
