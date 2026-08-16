import json
from kubernetes import client, config
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dora-k8s-server")

def get_k8s_client():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    return client.CoreV1Api()

@mcp.tool()
def get_pod_status(namespace: str = "default") -> str:
    """Retourne l'état actuel de tous les pods dans un namespace"""
    v1 = get_k8s_client()
    pods = v1.list_namespaced_pod(namespace=namespace)
    result = [{"name": p.metadata.name, "status": p.status.phase, "ready": all(c.ready for c in (p.status.container_statuses or [])), "restarts": sum(c.restart_count for c in (p.status.container_statuses or []))} for p in pods.items]
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_recent_events(namespace: str = "default") -> str:
    """Retourne les événements K8s récents dans un namespace"""
    v1 = get_k8s_client()
    events = v1.list_namespaced_event(namespace=namespace)
    result = [{"timestamp": str(e.last_timestamp), "type": e.type, "reason": e.reason, "resource": e.involved_object.name, "message": e.message, "count": e.count} for e in events.items]
    result.sort(key=lambda x: x["timestamp"], reverse=True)
    return json.dumps(result[:20], ensure_ascii=False, indent=2)

@mcp.tool()
def get_pod_logs(pod_name: str, namespace: str = "default", lines: int = 50) -> str:
    """Retourne les logs récents d'un pod spécifique"""
    v1 = get_k8s_client()
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, tail_lines=lines)
        return logs
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

@mcp.tool()
def get_crashed_pods(namespace: str = "default") -> str:
    """Retourne la liste des pods en erreur ou crashés"""
    v1 = get_k8s_client()
    pods = v1.list_namespaced_pod(namespace=namespace)
    crashed = []
    for p in pods.items:
        for cs in (p.status.container_statuses or []):
            if cs.restart_count > 0 or p.status.phase in ["Failed", "Unknown"]:
                crashed.append({"name": p.metadata.name, "phase": p.status.phase, "restarts": cs.restart_count, "ready": cs.ready})
    return json.dumps(crashed, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
