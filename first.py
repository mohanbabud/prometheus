import boto3

#ec2 = boto3.client('ec2',aws_access_key_id=AKIA4BKIPYPIOVAYV6MZ,aws_secret_access_key=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,region_name='us-east-1')
#ec2 = boto3.client("ec2")
client = boto3.client("ec2")
response = client.describe_volumes()
print(response)