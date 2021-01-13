from playhouse.postgres_ext import *
from datetime import datetime
from database.models.base import BaseModel

class LendingAssets(BaseModel):
    time = DateTimeField(default=datetime.utcnow)
    currency = CharField()
    assets = JSONField()