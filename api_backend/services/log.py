import pymongo
import bson
import pytz
from datetime import datetime
from constants import EventTargetTypes, EventTypes
from config import Config

class LogService():
  def __init__(
    self,
    mongo_client=pymongo.MongoClient(Config.MONGO_MAIN_URI),
  ):
    self.mongo_client = mongo_client
    self.db = self.mongo_client.get_database()
    self.collection = self.db.eventlogs
    return
  
  def log_event(
    self, 
    user_id: bson.ObjectId, 
    event_type: EventTypes,
    target_id: bson.ObjectId=None,
    target_type: EventTargetTypes=None,
    old_data=None,
    new_data=None,
  ):
    log = {
      "user_id": user_id,
      "event_type": event_type,
      "event_time": datetime.now(pytz.UTC),
    }
    if target_id:
      log["target_id"] = target_id
      log["target_type"] = target_type
      
    if old_data or new_data:
      log["change"] = {
        "old_data": old_data,
        "new_data": new_data,
      }
      
    self.collection.insert_one(log)
    return
  