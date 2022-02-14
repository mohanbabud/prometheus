def vol(event, context):
    pass


import logging
import boto3
import json
import os
from pprint import pprint
# Initialize boto3 cloudwatch and ec2

cloudwatch = boto3.client("cloudwatch")
ec2 = boto3.client("ec2")
response = ec2.describe_volumes()

#Define Dictionary to store volume status and Volume States
volumesbyid = {}

#Define Dictionary for State and Status Mapping to Numbers

volumestatuses = {'ok': 0, 'impaired': 1, 'warning': 2, 'passed': 3, 'insufficient-data': 4}
volumestates = {'available': 0, 'creating': 1, 'deleted': 2, 'deleting': 3, 'in-use': 4}
volumes = {}

#
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
    Status2 = VolumeStatus['Status']
    info = volumesbyid.setdefault(VolumeId, {})
    statecode = volumestatuses.get(Status2, -1)
    info['vol_status'] = statecode

# *** Below Block is to get io-enabled status***##


#    for detail in details:
#        if detail['Name'] == 'io-enabled':
#            VolumeStatus = detail['Status']
#            statecode = volumestatuses.get(VolumeStatus, -1)
#            info = volumesbyid.setdefault(VolumeId, {})
#            info['volume_status'] = statecode
items = volumesbyid.items()

for x, v in volumesbyid.items():
    if 'InstanceId' in v:
        volume_state = v['volume_state']
        volume_status = v['vol_status']
        print('Yes')


        def put_ec2_volume_metrics(VolumeId, InstanceId):

            #            namespace = 'EBS'
            #            dimensions = [dict(Name='InstanceId',value=InstanceId),dict(Name='VolumeID',Value=VolumeId)]
            #            metrics = [(MetricName="volume_state","Value"=volume_state,Dimesnsions=dimensions)]
            #            cloudwatch.put_metric_data(Namespace=namespace,MetricData=metrics)
            #
            print("yes")
    else:
        print('No')
#       def put_ec2_volume_metrics(volumeid,volum_state, volume_status):
#            namespace = 'EBS'
##            dimensions = [volumesbyid(Name='VolumeID', Value=VolumeId)]
#            metrics = [volumesbyid(MetricName='volume_state', value=volume_state, Dimesnsions=dimensions),]

#            cloudwatch.put_metric_data(Namespace=namespace, MetricData=metrics)


print('=' * 30)
pprint(volumesbyid)
