import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

TEMP_METRIC = "ibbq_temp_f"
BATTERY_METRIC = "ibbq_battery"
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
    push_to_gateway(DESTINATIION,"battery level collector", registry)

