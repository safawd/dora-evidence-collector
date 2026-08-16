import requests
import json
import urllib3
urllib3.disable_warnings()
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dora-argocd-server")

ARGOCD_SERVER = "https://localhost:9090"
ARGOCD_PASSWORD = "WCTmExSyXoKMNv-b"

def get_token():
    try:
        response = requests.post(f"{ARGOCD_SERVER}/api/v1/session", json={"username": "admin", "password": ARGOCD_PASSWORD}, verify=False, timeout=10)
        return response.json().get("token")
    except:
        return None

@mcp.tool()
def get_last_deployment(app_name: str = "banking-app") -> str:
    """Retourne les détails du dernier déploiement (commit, heure)"""
    token = get_token()
    if not token:
        return "❌ Impossible de se connecter à ArgoCD"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{ARGOCD_SERVER}/api/v1/applications/{app_name}", headers=headers, verify=False, timeout=10)
    app_data = response.json()
    status = app_data.get("status", {})
    history = status.get("history", [])
    last = history[-1] if history else {}
    result = {"app_name": app_name, "sync_status": status.get("sync", {}).get("status"), "revision": status.get("sync", {}).get("revision"), "last_deployment": {"deployed_at": last.get("deployedAt"), "revision": last.get("revision")}}
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_sync_status(app_name: str = "banking-app") -> str:
    """Retourne l'état actuel de synchronisation de l'application"""
    token = get_token()
    if not token:
        return "❌ Impossible de se connecter à ArgoCD"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{ARGOCD_SERVER}/api/v1/applications/{app_name}", headers=headers, verify=False, timeout=10)
    app_data = response.json()
    status = app_data.get("status", {})
    result = {"app_name": app_name, "sync_status": status.get("sync", {}).get("status"), "health_status": status.get("health", {}).get("status"), "revision": status.get("sync", {}).get("revision")}
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_argocd_events(app_name: str = "banking-app") -> str:
    """Retourne les événements récents ArgoCD pour une application"""
    token = get_token()
    if not token:
        return "❌ Impossible de se connecter à ArgoCD"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{ARGOCD_SERVER}/api/v1/applications/{app_name}/events", headers=headers, verify=False, timeout=10)
    events = response.json().get("items", []) or []
    result = [{"timestamp": e.get("lastTimestamp"), "type": e.get("type"), "reason": e.get("reason"), "message": e.get("message")} for e in events]
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
