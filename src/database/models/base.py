from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase

db = PooledPostgresqlExtDatabase('kubot', user='kubot',
                           password='kubot', host='postgres',
                           port=5432, max_connections=8, stale_timeout=300)

class BaseModel(Model):
    class Meta:
        database = db

