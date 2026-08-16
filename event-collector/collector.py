from database import init_db, get_all_events
from sources.k8s_source import collect_k8s_events
from sources.argocd_source import collect_argocd_events
from sources.prometheus_source import collect_prometheus_alerts, collect_prometheus_metrics
from sources.loki_source import collect_loki_logs, collect_all_errors
import sys

def run_collector(namespace="default"):
    print("🚀 Démarrage du DORA Event Collector")
    print("=" * 60)
    
    # Initialiser la base de données
    init_db()
    
    total = 0
    
    # Collecter depuis K8s
    print("\n📡 Collecte depuis Kubernetes...")
    total += collect_k8s_events(namespace=namespace)
    
    # Collecter depuis ArgoCD
    print("\n📡 Collecte depuis ArgoCD...")
    total += collect_argocd_events(app_name="banking-app")
    
    # Collecter depuis Prometheus
    print("\n📡 Collecte depuis Prometheus...")
    total += collect_prometheus_alerts()
    total += collect_prometheus_metrics(query="up")
    
    # Collecter depuis Loki
    print("\n📡 Collecte depuis Loki...")
    total += collect_loki_logs(app="sequence-generator", minutes=60)
    total += collect_all_errors(minutes=60)
    
    print("\n" + "=" * 60)
    print(f"✅ Total : {total} événements collectés")
    
    # Afficher les 10 derniers événements
    events = get_all_events()[:10]
    print(f"\n📋 10 derniers événements :")
    print("-" * 80)
    for e in events:
        print(f"[{e[1][:19]}] [{e[2]:10}] [{e[3]:20}] {e[5][:30]} - {e[6][:50]}")

if __name__ == "__main__":
    namespace = sys.argv[1] if len(sys.argv) > 1 else "default"
    run_collector(namespace=namespace)
