import datetime
import logging
import boto3


def get_available_eks_clusters():
    eks = boto3.client('eks')
    exclude_eks_clusters = ['dev', 'staging']
    eks_clusters = []

    response = eks.list_clusters()

    for cluster in response['clusters']:
        if cluster not in exclude_eks_clusters:
            eks_clusters.append(cluster)
    logging.warning(f"The following eks clusters were found: {eks_clusters}")

    return eks_clusters


def push_custom_metric(cluster):
    cloudwatch = boto3.client('cloudwatch')

    namespace = 'Custom/EKSClusters'
    metric_name = "eks_cluster_running"
    unit = 'Count'

    dimensions = [{'Name': 'cluster', 'Value': cluster}]

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': metric_name,
                'Dimensions': dimensions,
                'Timestamp': datetime.datetime.now(),
                'Value': 1,
                'Unit': unit
            },
        ],
        Namespace=namespace
    )


def main():
    clusters = get_available_eks_clusters()
    for cluster in clusters:
        push_custom_metric(cluster)


if __name__ == "__main__":
    main()
