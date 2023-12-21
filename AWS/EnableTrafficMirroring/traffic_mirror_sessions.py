#!/usr/bin/python3

import os
import logging
import boto3
from boto3 import exceptions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tm_filter_id = os.environ.get('TM_FILTER_ID')
tm_target_id = os.environ.get('TM_TARGET_ID')
ec2_name_tag = os.environ.get('CLUSTER_NAME')

# Initialize clients for EC2 and EC2 resource
ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')


def get_ec2_id(event: dict):
    """Get the EC2 instance ID."""
    try:
        instance_id = event['detail']['EC2InstanceId']
        logger.info('Instance ID: {}'.format(instance_id))
    except KeyError as err:
        logger.error('Could not get EC2 instance ID from Event {}'.format(err))
        raise
    return instance_id


def get_ec2_primary_eni_id(instance_id: str):
    """Get the instance Primary ENI ID."""
    try:
        instance = ec2_resource.Instance(instance_id)
        eni_id = instance.network_interfaces[0].id
        logger.info('Instance ENI ID: {}'.format(eni_id))
    except Exception as err:
        logger.error(
            'Could not get {} EC2 instance. Error: {}'.format(instance_id, err))
        raise
    return eni_id


def create_tm_session(eni_id: str):
    """Add the ENI to traffic mirroring."""
    logger.info("Adding {} to the Traffic Mirroring".format(eni_id))
    try:
        response = ec2.create_traffic_mirror_session(
            NetworkInterfaceId=eni_id,
            TrafficMirrorTargetId=tm_target_id,
            TrafficMirrorFilterId=tm_filter_id,
            SessionNumber=1,
            Description=ec2_name_tag + '-' + eni_id,
            TagSpecifications=[
                {
                    'ResourceType': 'traffic-mirror-session',
                    'Tags': [
                        {
                            'Key': 'clusterName',
                            'Value': ec2_name_tag
                        }
                    ]
                }
            ],
        )
    except exceptions.Boto3Error as err:
        logger.info(
            "Couldn't add {} to traffic mirroring session. Error: {}".format(eni_id, err))
        response = 'Failed to receive response'
    logger.info("Response: {}".format(response))


def lambda_handler(event, _):
    """Function launch."""
    logger.info("Received event: {}".format(event))
    ec2_id = get_ec2_id(event)
    eni_id = get_ec2_primary_eni_id(ec2_id)
    return create_tm_session(eni_id)
