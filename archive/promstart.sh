#!/bin/bash
screen -d -m /etc/prometheus/prometheus --config.file /etc/prometheus/prometheus.yml
screen -d -m /etc/pushgateway/pushgateway
