from prometheus_client import Gauge
from json import load

with open("build_info.json", "r") as buildinfo:
    info = load(buildinfo)

metric = info['appname'] + "_build_info"
build_info = Gauge(metric, 'Build Information',
                   ['branch', 'goversion', 'revision', 'version'])

build_info.labels(info['branch'], 'none', info['revision'], info['version']).set(1)