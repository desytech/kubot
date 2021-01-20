from playhouse.postgres_ext import *
from datetime import datetime
from database.models.base import BaseModel

class FundingMarket(BaseModel):
    time = DateTimeField(default=datetime.utcnow)
    currency = CharField()
    market = JSONField()
