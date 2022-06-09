#!/usr/bin/env python3
import sys
import yaml
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()


def to_bool(s: str) -> bool:
    return s.lower() in ["true", "1", "t", "y", "yes"]


enabled = True if len(sys.argv) < 2 else to_bool(sys.argv[1])
cfmap = dict(namespace="kube-system", name="kube-proxy")
kube_proxy_config = v1.read_namespaced_config_map(**cfmap, pretty=True)

conf = yaml.safe_load(kube_proxy_config.data["config.conf"])
changed = conf["ipvs"]["strictARP"] != enabled
conf["ipvs"]["strictARP"] = enabled
kube_proxy_config.data["config.conf"] = yaml.dump(conf)

v1.patch_namespaced_config_map(
    **cfmap,
    body=kube_proxy_config,
    pretty=True,
)

print({"strictARP": enabled})
if changed:
    print("changed")
