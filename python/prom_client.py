import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

def prom_temperature(temp):
    registry = CollectorRegistry()
    g = Gauge("ibbq_temp_f", "Temperature from iBBQ probe (F)", registry=registry)
    g.set(temp)
    return registry

def push_temperature(temp,probe):
    registry = prom_temperature(temp)
    if probe == 1:
        push_to_gateway("localhost:9091", "temperature collector probe 1", registry)
    else:
        push_to_gateway("localhost:9091", "temperature collector probe 2", registry)

def prom_battery(pct):
    pass

def push_battery(pct):
    pass
