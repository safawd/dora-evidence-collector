import requests
import json
from database import insert_event

PROMETHEUS_URL = "http://localhost:9091"

def collect_prometheus_alerts():
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/alerts",
            timeout=10
        )
        alerts = response.json().get("data", {}).get("alerts", [])
        
        count = 0
        for alert in alerts:
            labels = alert.get("labels", {})
            insert_event(
                source="prometheus",
                event_type="Alert",
                namespace=labels.get("namespace", "unknown"),
                resource_name=labels.get("alertname", "unknown"),
                message=alert.get("annotations", {}).get("description", ""),
                severity=labels.get("severity", "INFO").upper(),
                raw_data=json.dumps(alert)
            )
            count += 1
        
        print(f"✅ Prometheus: {count} alertes collectées")
        return count
    except Exception as e:
        print(f"❌ Prometheus error: {e}")
        return 0

def collect_prometheus_metrics(query="up"):
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        results = response.json().get("data", {}).get("result", [])
        
        count = 0
        for result in results:
            metric = result.get("metric", {})
            value = result.get("value", [None, None])[1]
            
            if value == "0":
                insert_event(
                    source="prometheus",
                    event_type="ServiceDown",
                    namespace=metric.get("namespace", "unknown"),
                    resource_name=metric.get("pod", metric.get("job", "unknown")),
                    message=f"Service is DOWN (up=0)",
                    severity="ERROR",
                    raw_data=json.dumps(result)
                )
                count += 1
        
        print(f"✅ Prometheus metrics: {count} anomalies détectées")
        return count
    except Exception as e:
        print(f"❌ Prometheus metrics error: {e}")
        return 0
