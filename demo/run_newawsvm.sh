#!/bin/bash

# This script runs newawsvm command to display status, boot 2 virtual machines requesting the same name, show their status, then stops them
# -colliner
# demo

echo "Please open file before using"
echo "press enter when ready, or CTRL-C to exit"
read i
cms newawsvm status
echo "Status should be displayed of all nodes on aws and looked for test_cloudmesh0 and test_cloudmesh01 but did not find any nodes with those names" 
echo "press enter when ready"
read i
cms newawsvm boot
echo "just booted test_cloudmesh0"
echo "press enter when ready"
read i
cms newawsvm boot
echo "just tried to boot another node with the same name"
echo "press enter when ready"
read i
cms newawsvm status
echo "Showing updated status"
echo "press enter when ready"
read i
cms newawsvm stop
echo "just stopped both nodes"
