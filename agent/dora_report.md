# RAPPORT D'INCIDENT DORA (Digital Operational Resilience Act)
**Entité Financière :** Infrastructure Bancaire Centrale  
**Date du rapport :** 16 août 2026  
**Statut de l'incident :** Clôturé / En cours de stabilisation  

---

## 1. Résumé Exécutif
- **Description de l'incident :** Perte critique de la haute disponibilité du plan de contrôle Kubernetes (`Control Plane`) et des composants fondamentaux de l'infrastructure (`etcd`, `kube-scheduler`, `kube-controller-manager`, `kube-proxy`). En parallèle, des instabilités chroniques ont été observées sur les microservices applicatifs et l'outil de déploiement ArgoCD.
- **Date et heure de détection :** 2026-08-16 à 13:18:25 UTC (première occurrence) avec une récurrence confirmée à 13:46:46 UTC.
- **Sévérité :** **CRITIQUE** (Impact majeur sur la résilience opérationnelle et la continuité des services financiers).
- **Services impactés :** 
  - Plan de contrôle Kubernetes (etcd, scheduler, controller-manager, proxy).
  - Outils de supervision et de déploiement (`prometheus-grafana`, `argocd-applicationset-controller`).
  - Microservices métiers (fort taux de redémarrages constatés sur les pods applicatifs, témoignant d'une instabilité sous-jacente).

---

## 2. Timeline Détaillée
- **2026-08-16T13:18:25Z (Première détection) :** 
  - Alerte initiale de Prometheus : Perte de cibles critiques dans le namespace `kube-system` (`etcd`, `kube-proxy`, `kube-scheduler`, `kube-controller-manager`) et dans `monitoring` (`prometheus-grafana`).
  - Détection de la saturation de nœud (`NodeSystemSaturation`, charge CPU > 2 sur 15 min, pic à 3.29).
  - Signalement de pods en `CrashLoopBackOff` (`argocd-applicationset-controller` et `prometheus-grafana`).
  - Passage des services du plan de contrôle à l'état `DOWN (up=0)` (IDs 17 à 21).
- **13:18 - 13:46 UTC (Phase d'escalade) :** 
  - Persistance des instances injoignables pendant plus de 15 minutes.
- **2026-08-16T13:46:46Z (Seconde vague / Confirmation) :** 
  - Nouvelle série d'alertes confirmant l'indisponibilité continue des composants du control plane et des services de supervision (IDs 34 à 53).

---

## 3. Analyse de l'Impact
- **Services bancaires affectés :** Bien que les pods des microservices (`account-service`, `fund-transfer`, `transaction-service`, `user-service`, `api-gateway`) rapportent un statut `Running` avec un niveau élevé de redémarrages cumulés (ex: `user-service` à 120 restarts, `transaction-service` à 78 restarts), l'intégrité globale de la plateforme est compromise par la perte du plan de contrôle Kubernetes.
- **Durée d'indisponibilité estimée :** > 30 minutes de dégradation sévère de l'infrastructure de gestion.
- **Transactions potentiellement impactées :** Risque élevé de rejet ou de timeout sur les flux de paiements (`fund-transfer`) et les requêtes de comptes en raison de la saturation des nœuds et de l'instabilité des passerelles API.

---

## 4. Cause Racine (RCA)
- **Cause principale identifiée :** Saturation critique des ressources des nœuds de l'infrastructure (`NodeSystemSaturation` avec une charge système par cœur atteignant 3.29), entraînant le gel ou l'éviction des composants critiques du système (`etcd`, `kube-scheduler`, `kube-controller-manager`).
- **Facteurs contributifs :**
  - Instabilité applicative chronique matelassée par un nombre anormalement élevé de redémarrages de pods (restarts excessifs sur les services métiers : `user-service`, `transaction-service`, `account-service`), pesant sur la stabilité globale de l'hyperviseur/cluster.
  - Défaillance concomitante des outils de supervision (`Prometheus/Grafana` en boucle de crash), réduisant la visibilité en temps réel des équipes d'exploitation.
- **Chaîne de causalité :** Surcharge de calcul / fuite de ressources -> Saturation du nœud -> Perte de réactivité des composants du Control Plane Kubernetes (`etcd` / `kube-proxy`) -> Indisponibilité des services système -> Effet domino sur la supervision et les contrôleurs de déploiement.

---

## 5. Actions de Remédiation
- **Actions immédiates prises :** 
  - Identification des services en échec via les sondes de Prometheus.
  - Collecte des métriques d'infrastructure et des états de pods.
- **Actions correctives planifiées :**
  - Redémarrage à froid et rééquilibrage de la charge sur les nœuds du cluster Kubernetes.
  - Investigation approfondie sur les causes des `CrashLoopBackOff` des pods `argocd` et `prometheus-grafana`.
- **Mesures préventives :**
  - Ajustement des limites et des requêtes de ressources (`CPU/Memory Requests & Limits`) pour l'ensemble des microservices afin d'éviter la saturation des nœuds.
  - Optimisation des sondes de vivacité (`liveness probes`) et de préparation (`readiness probes`).

---

## 6. Conformité DORA
- **Article 17 (Gestion des incidents TIC) :** 
  - L'incident a fait l'objet d'un enregistrement exhaustif des données de télémétrie (logs Loki, métriques Prometheus, états K8s). Les procédures de détection et de consignation ont permis de documenter l'événement avec précision.
- **Article 18 (Classification des incidents TIC) :** 
  - Cet incident est qualifié d'**incident TIC majeur** au sens de DORA, impactant la continuité des services financiers essentiels (interruption des composants d'infrastructure critiques, nombre de clients/transactions potentiellement touchés, criticité des actifs affectés).
- **Article 19 (Notification des incidents TIC graves) :** 
  - Compte tenu de la criticité de la défaillance du plan de contrôle et des services bancaires de premier plan, une analyse d'éligibilité pour une notification aux autorités compétentes (ex: BCE / Autorité nationale de régulation) doit être immédiatement initiée conformément aux seuils réglementaires DORA.

---

## 7. Recommandations
- **Améliorations de résilience opérationnelle :** 
  - Mettre en place une architecture multi-maîtres (`multi-master control plane`) hautement résiliente pour éviter tout point de défaillance unique (SPOF) sur `etcd` et le plan de contrôle.
- **Renforcement du monitoring :** 
  - Découpler l'infrastructure de supervision du cluster principal ou garantir sa haute disponibilité prioritaire pour éviter sa cécité lors des crises de saturation.
- **Tests de résilience recommandés :** 
  - Réaliser des tests de chaos engineering (`Chaos Engineering`) ciblant spécifiquement la résilience d'`etcd` et la saturation des nœuds pour valider les mécanismes de bascule automatique.