# ibbqgraph - Python3-based RPi3 integration with iBBQ probe and prometheus pushgateway

## Description

Simple metrics collector for the Inkbird IBT-2X Bluetooth thermometer, running on Raspberry Pi 3 (ARM7 architecture). Server code written in Python3. Metrics exported to prometheus pushgateway.

I personally scrape the Pushgateway port with Prometheus, then run a Grafana frontend to prettify the display

## Prometheus Metrics

```
ibbq_temp_f - current probe temperature (F)
ibbq_battery - current battery level
ibbq_temp - monitoring uptime
```

## Pushgateway Jobs

```
temperature+collector+probe+1
temperature+collector+probe+2
battery+level+collector
time+collector
```

## Prerequisites

1) Python3
2) prometheus* - https://prometheus.io/download/
3) pushgateway* - https://prometheus.io/download/
4) Inkbird IBT-2X
5) Raspberry Pi (I used a Pi 3)
6) Bluepy Python module - https://github.com/IanHarvey/bluepy
7) `screen` - https://linux.die.net/man/1/screen

* Download the version specific to your hardware's architecture. Ex: Get the armv7 distro for a Raspberry Pi 3

## Directions

1) Clone this repository
2) Ensure all prerequisites are installed/purchased
3) Ensure prometheus and pushgateway are configured correctly (see respective documentation for both) and running
    3a) If you are installing prometheus and pushgateway on the same hardware, you can have prometheus scrape localhost:9091 for all pushed metrics
    3b) You may choose to run prometheus and pushgateway as systemd services
4) Turn on the IBT-2X probe
4) Run `beginsmoke.sh`
5) Visit localhost:9091 to see the pushed metrics
6) Visit localhost:9090 to access prometheus and begin running queries

## Notes

Grafana systemd service is started at boot 
 - Check status with `sudo systemctl status grafana-server`

Prometheus and Pushgateway are also configured at startup
 - prometheus.service
 - pushgateway.service
