from playhouse.postgres_ext import *
from datetime import datetime
from database.models.base import BaseModel

class CategoryCurrency(BaseModel):
    time = DateTimeField(default=datetime.utcnow)
    category = CharField()
    items = JSONField()