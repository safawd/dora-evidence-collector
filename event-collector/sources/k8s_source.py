from kubernetes import client, config
from database import insert_event
import json

def collect_k8s_events(namespace="default"):
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    
    v1 = client.CoreV1Api()
    events = v1.list_namespaced_event(namespace=namespace)
    
    count = 0
    for event in events.items:
        severity = "WARNING" if event.type == "Warning" else "INFO"
        insert_event(
            source="kubernetes",
            event_type=event.reason or "Unknown",
            namespace=namespace,
            resource_name=event.involved_object.name,
            message=event.message or "",
            severity=severity,
            raw_data=json.dumps({
                "reason": event.reason,
                "count": event.count,
                "first_time": str(event.first_timestamp),
                "last_time": str(event.last_timestamp)
            })
        )
        count += 1
    
    print(f"✅ K8s: {count} événements collectés")
    return count
