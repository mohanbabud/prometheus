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
volumestatuses = {'ok': 0, 'impaired': 1, 'warning': 2, 'passed': 3, 'insufficient-data': 4}
volumestates = {'available': 0, 'creating': 1, 'deleted': 2, 'deleting': 3, 'in-use': 4}
volumes = {}


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
           InstanceId = k['InstanceId']
           info3 = volumesbyid.setdefault(volid, {})
           info3['InstanceId'] = InstanceId


response = ec2.describe_volume_status()

for volume in response['VolumeStatuses']:
    VolumeId = volume['VolumeId']
    VolumeStatus = volume['VolumeStatus']
    details = VolumeStatus['Details']
    for detail in details:
        if detail['Name'] == 'io-enabled':
            VolumeStatus = detail['Status']
            statecode = volumestatuses.get(VolumeStatus, -1)
            info = volumesbyid.setdefault(VolumeId, {})
            info['volume_status'] = statecode
for x,v in volumesbyid.items():
    if 'InstanceId' in v:
       def put_ec2_volume_metrics(instanceid,volumeid,volume_state,volume_status):
           namespace='EBS'
           dimensions = [volumesbyid(Name='VolumeID',Value=VolumeId)]
           metrics = [ volumesbyid(MetricName='volume_state',value=volume_state,Dimesnsions=dimensions)]
           cloudwatch.put_metric_data(Namespace=namespace,MetricData=metrics)
           print(metrics)
    else:
        def put_ec2_volume_metrics(volumeid, volume_state, volume_status):
            namespace = 'EBS'
            dimensions = [volumesbyid(Name='VolumeID', Value=VolumeId)]
            metrics = [volumesbyid(MetricName='volume_state', value=volume_state, Dimesnsions=dimensions)]
            print(metrics)
            cloudwatch.put_metric_data(Namespace=namespace, MetricData=metrics)


print('=' * 30)
pprint(volumesbyid)