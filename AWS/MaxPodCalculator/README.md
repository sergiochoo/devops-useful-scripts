The script to check how many pods can be allocated on the EKS worker node.

Usage:
AWS_PROFILE=<profile name> ./max-pods-calculator.sh --instance-type t2.micro --cni-version 1.7.5
(Adjust the instance type and cni version for you specific workload)