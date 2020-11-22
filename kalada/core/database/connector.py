from umongo import Instance

from kalada.core.database.client import Mongo

mongo = Mongo()
instance = Instance(mongo.db)
