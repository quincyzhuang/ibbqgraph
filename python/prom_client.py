import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

TEMP_METRIC = "ibbq_temp_f"
BATTERY_METRIC = "ibbq_battery"
TIME_METRIC = "ibbq_time"
DESTINATION = "localhost:9091"

def prom_temperature(temp):
    registry = CollectorRegistry()
    g = Gauge(TEMP_METRIC, "Temperature from iBBQ probe (F)", registry=registry)
    g.set(temp)
    return registry

def push_temperature(temp,probe):
    registry = prom_temperature(temp)
    if probe == 1:
        push_to_gateway(DESTINATION, "temperature collector probe 1", registry)
    else:
        push_to_gateway(DESTINATION, "temperature collector probe 2", registry)

def prom_battery(pct):
    registry = CollectorRegistry()
    g = Gauge(BATTERY_METRIC, "Battery from iBBQ probe", registry=registry)
    g.set(pct)
    return registry

def push_battery(pct):
    registry = prom_battery(pct)
    push_to_gateway(DESTINATION,"battery level collector", registry)

def prom_time(sec):
    registry = CollectorRegistry()
    g = Gauge(TIME_METRIC, "iBBQ monitoring uptime", registry=registry)
    g.set(sec)
    return registry

def push_time(sec):
    registry = prom_time(sec)
    push_to_gateway(DESTINATION,"time collector", registry)


