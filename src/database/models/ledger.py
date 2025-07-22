from playhouse.postgres_ext import *
from datetime import datetime
from database.models.base import BaseModel

class LedgerAssets(BaseModel):
    time = DateTimeField(default=datetime.utcnow)
    ledger = JSONField()