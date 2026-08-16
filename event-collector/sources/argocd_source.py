import requests
import json
import urllib3
urllib3.disable_warnings()
from database import insert_event

ARGOCD_SERVER = "https://localhost:9090"

def get_argocd_token(username="admin", password="WCTmExSyXoKMNv-b"):
    try:
        response = requests.post(
            f"{ARGOCD_SERVER}/api/v1/session",
            json={"username": username, "password": password},
            verify=False,
            timeout=10
        )
        return response.json().get("token")
    except Exception as e:
        print(f"❌ ArgoCD auth error: {e}")
        return None

def collect_argocd_events(app_name="banking-app"):
    token = get_argocd_token()
    
    if not token:
        print("❌ Impossible de se connecter à ArgoCD")
        return 0
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{ARGOCD_SERVER}/api/v1/applications/{app_name}/events",
            headers=headers,
            verify=False,
            timeout=10
        )
        events = response.json().get("items", [])
        
        count = 0
        for event in events:
            insert_event(
                source="argocd",
                event_type=event.get("reason", "Unknown"),
                namespace="argocd",
                resource_name=app_name,
                message=event.get("message", ""),
                severity="WARNING" if event.get("type") == "Warning" else "INFO",
                raw_data=json.dumps(event)
            )
            count += 1
        
        print(f"✅ ArgoCD: {count} événements collectés")
        return count
    except Exception as e:
        print(f"❌ ArgoCD error: {e}")
        return 0
