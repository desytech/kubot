from playhouse.postgres_ext import *
from datetime import datetime
from database.models.base import BaseModel

class SymbolAssets(BaseModel):
    time = DateTimeField(default=datetime.utcnow)
    symbol = JSONField()