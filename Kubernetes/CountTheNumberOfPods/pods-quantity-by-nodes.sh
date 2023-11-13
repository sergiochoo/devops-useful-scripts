#!/bin/sh

all_nodes=$(kubectl get nodes -o=custom-columns='NAME:metadata.name' --no-headers)

for node in $all_nodes
do
    quantity=$(kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName="$node" --no-headers | wc -l)
    echo "$quantity" "|" "$node";
done
