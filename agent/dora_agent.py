from google import genai
from google.genai import types
import sys
import os
import json

sys.path.append('/root/DORA-PFE/event-collector')
sys.path.append('/root/DORA-PFE/mcp-servers')

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def collect_infrastructure_data():
    data = {}
    
    try:
        from mcp_sqlite_server import get_stats, get_incident_timeline, get_events_by_severity
        data['stats'] = json.loads(get_stats())
        data['incident_timeline'] = json.loads(get_incident_timeline(hours=24))
        data['errors'] = json.loads(get_events_by_severity("ERROR"))
        data['warnings'] = json.loads(get_events_by_severity("WARNING"))
        print("✅ Données SQLite collectées")
    except Exception as e:
        print(f"❌ SQLite error: {e}")
        data['stats'] = {}
        data['incident_timeline'] = []
        data['errors'] = []
        data['warnings'] = []

    try:
        from mcp_k8s_server import get_pod_status, get_crashed_pods, get_recent_events
        data['pod_status'] = json.loads(get_pod_status('default'))
        data['crashed_pods'] = json.loads(get_crashed_pods('default'))
        data['k8s_events'] = json.loads(get_recent_events('default'))
        print("✅ Données K8s collectées")
    except Exception as e:
        print(f"❌ K8s error: {e}")
        data['pod_status'] = []
        data['crashed_pods'] = []
        data['k8s_events'] = []

    try:
        from mcp_argocd_server import get_last_deployment, get_sync_status
        data['last_deployment'] = json.loads(get_last_deployment('banking-app'))
        data['sync_status'] = json.loads(get_sync_status('banking-app'))
        print("✅ Données ArgoCD collectées")
    except Exception as e:
        print(f"❌ ArgoCD error: {e}")
        data['last_deployment'] = {}
        data['sync_status'] = {}

    return data

def run_dora_agent():
    print("🤖 Démarrage de l'Agent DORA avec Gemini")
    print("=" * 60)

    print("\n📡 Collecte des données infrastructure...")
    infra_data = collect_infrastructure_data()

    prompt = f"""Tu es un expert en conformité DORA (Digital Operational Resilience Act) de l'Union Européenne.

Voici les données collectées depuis l'infrastructure bancaire :

## Statistiques globales
{json.dumps(infra_data.get('stats', {}), indent=2, ensure_ascii=False)}

## Timeline des incidents (24h)
{json.dumps(infra_data.get('incident_timeline', []), indent=2, ensure_ascii=False)}

## Erreurs détectées
{json.dumps(infra_data.get('errors', []), indent=2, ensure_ascii=False)}

## Warnings détectés
{json.dumps(infra_data.get('warnings', []), indent=2, ensure_ascii=False)}

## État des pods Kubernetes
{json.dumps(infra_data.get('pod_status', []), indent=2, ensure_ascii=False)}

## Pods crashés
{json.dumps(infra_data.get('crashed_pods', []), indent=2, ensure_ascii=False)}

## Événements K8s récents
{json.dumps(infra_data.get('k8s_events', []), indent=2, ensure_ascii=False)}

## Dernier déploiement ArgoCD
{json.dumps(infra_data.get('last_deployment', {}), indent=2, ensure_ascii=False)}

## Statut de synchronisation ArgoCD
{json.dumps(infra_data.get('sync_status', {}), indent=2, ensure_ascii=False)}

---

Sur la base de ces données, génère un rapport d'incident DORA complet et structuré :

# RAPPORT D'INCIDENT DORA

## 1. Résumé Exécutif
- Description de l'incident
- Date et heure de détection
- Sévérité (Critique/Majeur/Mineur)
- Services impactés

## 2. Timeline Détaillée
- Chronologie précise des événements
- Première détection
- Escalade
- Résolution

## 3. Analyse de l'Impact
- Services bancaires affectés
- Durée d'indisponibilité estimée
- Nombre de transactions potentiellement impactées

## 4. Cause Racine (RCA)
- Cause principale identifiée
- Facteurs contributifs
- Chaîne de causalité

## 5. Actions de Remédiation
- Actions immédiates prises
- Actions correctives planifiées
- Mesures préventives

## 6. Conformité DORA
- Article 17 : Gestion des incidents TIC
- Article 18 : Classification des incidents
- Article 19 : Notification aux autorités compétentes

## 7. Recommandations
- Améliorations de résilience opérationnelle
- Renforcement du monitoring
- Tests de résilience recommandés

Génère ce rapport de manière professionnelle, précise et conforme aux exigences réglementaires DORA."""

    print("\n🔍 Analyse par Gemini en cours...\n")
    print("=" * 60)

    full_report = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-flash-lite-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.3
        )
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_report += chunk.text

    report_path = "/root/DORA-PFE/agent/dora_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_report)

    print("\n\n" + "=" * 60)
    print(f"✅ Rapport DORA généré et sauvegardé : {report_path}")

if __name__ == "__main__":
    run_dora_agent()
