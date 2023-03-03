from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder
from flask import request

class NotificationsActivities:
  def run():

    try:
      now = datetime.now(timezone.utc).astimezone()
      results = [{
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Kris Laiz',
        'message': 'Follow me',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [{
          'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
          'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'Worf',
          'message': 'This post has no honor!',
          'likes_count': 0,
          'replies_count': 0,
          'reposts_count': 0,
          'created_at': (now - timedelta(days=2)).isoformat()
        }],
      },    
      ]
      dict_subsegment={
          "type":"subsegment",
          "now": now.isoformat(),
          "results-sample-length": len(results)
      }

      subsegment = xray_recorder.begin_subsegment('subsegment-mock-data')
      subsegment.put_metadata('key', dict_subsegment, 'namespace')
      subsegment.put_annotation('hello', 'world')
      xray_recorder.end_subsegment()
    except Exception as e: 
      raise e
    
    finally:
      xray_recorder.end_subsegment()

    return results