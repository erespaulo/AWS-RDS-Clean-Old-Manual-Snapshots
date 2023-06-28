import boto3
import datetime
from os import getenv
from datetime import date
from datetime import datetime, timezone
from datetime import timedelta

client = boto3.client('rds')
ClientName = getenv('CLIENT_NAME')
today = (datetime.today()).date()
week_ago = today - timedelta(days=7)

def lambda_handler(event, context):
    snapshots_marker = ""
   
    while snapshots_marker != None:
        snapshots = client.describe_db_snapshots(Marker=snapshots_marker)
        
        if 'Marker' in snapshots:
            snapshots_marker = snapshots['Marker']
        else:
            snapshots_marker = None
            
        for snapshot in snapshots['DBSnapshots']:
            if snapshot["SnapshotType"] == "manual" and snapshot ["SnapshotCreateTime"].date() < week_ago:
                client.delete_db_snapshot(DBSnapshotIdentifier=snapshot["DBSnapshotIdentifier"])
