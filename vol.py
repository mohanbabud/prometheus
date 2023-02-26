def vol(event, context):
    pass


import logging
import boto3
import json
import os
from pprint import pprint

ec2 = boto3.client("ec2")
response = ec2.describe_volumes()
volumesbyid = {}
volumebyinsvol = {}
volumestatuses = {'ok': 0, 'impaired': 1, 'warning': 2,'insufficient-data': 3}
volumestates = {'available': 0, 'creating': 1, 'deleted': 2, 'deleting': 3, 'in-use': 4}
volumes = {}

print(response)
for volume in response['Volumes']:
    VolumeId = volume['VolumeId']
    Attach = volume['Attachments']
    info = volumes.setdefault(VolumeId, {})
    info['volume_state'] = volume['State']
    #    info['InstanceID'] = volume['InstanceId']
    for volid, volinfo in volumes.items():
        VolumeStatus = volinfo['volume_state']
        statecode = volumestates.get(VolumeStatus, -1)
        info2 = volumesbyid.setdefault(volid, {})
        info2['volume_state'] = statecode
        for k in Attach:
            if k['State'] == 'attached':
               InstanceId = k['InstanceId']
               info3 = volumesbyid.setdefault(volid, {})
               info3['InstanceId'] = InstanceId
            else:
                pass


response = ec2.describe_volume_status()

for volume in response['VolumeStatuses']:
    VolumeId = volume['VolumeId']
    VolumeStatus = volume['VolumeStatus']
    details = VolumeStatus['Details']
    Status2 = VolumeStatus['Status']
    info = volumesbyid.setdefault(VolumeId,{})
    statecode = volumestatuses.get(Status2, -1)
    info['vol_status'] = statecode


# Below Block is to fetch the IO Enabled Status

#    for detail in details:
#        if detail['Name'] == 'io-enabled':
#            VolumeStatus = detail['Status']
#            statecode = volumestatuses.get(VolumeStatus, -1)
#            info = volumesbyid.setdefault(VolumeId, {})
#            info['volume_status'] = statecode



print('=' * 30)
pprint(volumesbyid)
