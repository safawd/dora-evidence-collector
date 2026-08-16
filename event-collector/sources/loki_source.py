import requests
import json
from datetime import datetime, timedelta
from database import insert_event

LOKI_URL = "http://localhost:3101"

def collect_loki_logs(app="sequence-generator", minutes=60):
    try:
        end = datetime.utcnow()
        start = end - timedelta(minutes=minutes)
        
        params = {
            "query": f'{{app="{app}"}}',
            "start": str(int(start.timestamp() * 1e9)),
            "end": str(int(end.timestamp() * 1e9)),
            "limit": 100
        }
        
        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params=params,
            timeout=10
        )
        
        results = response.json().get("data", {}).get("result", [])
        
        count = 0
        for stream in results:
            for timestamp, line in stream.get("values", []):
                severity = "ERROR" if "ERROR" in line else "WARNING" if "WARN" in line else "INFO"
                insert_event(
                    source="loki",
                    event_type="Log",
                    namespace="default",
                    resource_name=app,
                    message=line[:500],
                    severity=severity,
                    raw_data=json.dumps({"stream": stream.get("stream", {})})
                )
                count += 1
        
        print(f"✅ Loki: {count} logs collectés pour {app}")
        return count
    except Exception as e:
        print(f"❌ Loki error: {e}")
        return 0

def collect_all_errors(minutes=60):
    try:
        end = datetime.utcnow()
        start = end - timedelta(minutes=minutes)
        
        params = {
            "query": '{namespace="default"} |= "ERROR"',
            "start": str(int(start.timestamp() * 1e9)),
            "end": str(int(end.timestamp() * 1e9)),
            "limit": 200
        }
        
        response = requests.get(
            f"{LOKI_URL}/loki/api/v1/query_range",
            params=params,
            timeout=10
        )
        
        results = response.json().get("data", {}).get("result", [])
        
        count = 0
        for stream in results:
            app_name = stream.get("stream", {}).get("app", "unknown")
            for timestamp, line in stream.get("values", []):
                insert_event(
                    source="loki",
                    event_type="Error",
                    namespace="default",
                    resource_name=app_name,
                    message=line[:500],
                    severity="ERROR",
                    raw_data=json.dumps({"stream": stream.get("stream", {})})
                )
                count += 1
        
        print(f"✅ Loki errors: {count} erreurs collectées")
        return count
    except Exception as e:
        print(f"❌ Loki errors error: {e}")
        return 0
