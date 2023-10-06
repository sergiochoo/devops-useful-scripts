import boto3
import datetime
import logging

EBS_VOLUME_METRIC_NAME = 'CustomMetric/EBSVolumes'


def get_available_ebs_volumes():
    ec2 = boto3.client('ec2')

    response = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}])
    volumes = response['Volumes']

    # Exclude the EBS volumes that contain the DONT_DELETE suffix in names
    volumes_names = []
    for volume in volumes:
        volume_name = next((tag['Value'] for tag in volume.get(
            'Tags', []) if tag['Key'] == 'Name'), None)
        if volume_name and "DONT_DELETE" not in volume_name:
            volumes_names.append(volume_name)
    logging.warning(
        "The following obsolete volumes were found: %s", volumes_names)

    return volumes_names


def push_custom_metric(volume_count):
    cloudwatch = boto3.client('cloudwatch')

    namespace = 'Custom/EBSVolumes'
    unit = 'Count'

    dimensions = [{'Name': 'MetricDimension', 'Value': 'EBSVolumes'}]

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': EBS_VOLUME_METRIC_NAME,
                'Dimensions': dimensions,
                'Timestamp': datetime.datetime.now(),
                'Value': volume_count,
                'Unit': unit
            },
        ],
        Namespace=namespace
    )


def main():
    volumes = get_available_ebs_volumes()
    volume_count = len(volumes)
    logging.warning("Found obsolete EBS volumes %s", volume_count)

    if volume_count > 0:
        push_custom_metric(volume_count)
        logging.warning("Custom metric pushed to CloudWatch.")
    else:
        logging.info("EBS volumes in the Available state weren't found.")


if __name__ == "__main__":
    main()
