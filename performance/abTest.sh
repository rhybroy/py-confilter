#!/bin/bash 

ab -c 50 -n 100 -p ./post -T 'application/x-www-form-urlencoded' http://192.168.41.222:9000/
