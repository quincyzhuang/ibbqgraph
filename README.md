# ibbqgraph - Python3 integreation with iBBQ probe and Prometheus Pushgateway

Prometheus ibb monitoring service

Metric: ibbq_temp_celcius
jobs: temperature collector probe 1/2

Grafana systemd service is started at boot 
 - Check status with sudo service grafana-server status

Prometheus and Pushgateway are also configured at startup
 - prometheus.service
 - pushgateway.service

1) Run python/readProbe.py to start temperature collection
2) Visit localhost:9090/9091 for prometheus/pushgateway
3) Visit :3000 for Grafana
