import sqlite3
import json
import sys
sys.path.append('/root/DORA-PFE/event-collector')
from mcp.server.fastmcp import FastMCP

DB_PATH = "/root/DORA-PFE/event-collector/dora_events.db"

mcp = FastMCP("dora-sqlite-server")

@mcp.tool()
def get_all_events(limit: int = 50) -> str:
    """Retourne tous les événements DORA collectés depuis l'infrastructure"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    result = [{"id": r[0], "timestamp": r[1], "source": r[2], "event_type": r[3], "namespace": r[4], "resource_name": r[5], "message": r[6], "severity": r[7]} for r in rows]
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_events_by_source(source: str) -> str:
    """Filtre les événements par source (kubernetes, argocd, prometheus, loki)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE source = ? ORDER BY timestamp DESC", (source,))
    rows = cursor.fetchall()
    conn.close()
    result = [{"id": r[0], "timestamp": r[1], "source": r[2], "event_type": r[3], "namespace": r[4], "resource_name": r[5], "message": r[6], "severity": r[7]} for r in rows]
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_events_by_severity(severity: str) -> str:
    """Filtre les événements par sévérité (ERROR, WARNING, INFO)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE severity = ? ORDER BY timestamp DESC", (severity,))
    rows = cursor.fetchall()
    conn.close()
    result = [{"id": r[0], "timestamp": r[1], "source": r[2], "event_type": r[3], "namespace": r[4], "resource_name": r[5], "message": r[6], "severity": r[7]} for r in rows]
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_incident_timeline(hours: int = 24) -> str:
    """Retourne la timeline complète des incidents triée par timestamp"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM events 
        WHERE timestamp >= datetime('now', '-' || ? || ' hours')
        AND severity IN ('ERROR', 'WARNING')
        ORDER BY timestamp ASC
    """, (hours,))
    rows = cursor.fetchall()
    conn.close()
    result = [{"id": r[0], "timestamp": r[1], "source": r[2], "event_type": r[3], "namespace": r[4], "resource_name": r[5], "message": r[6], "severity": r[7]} for r in rows]
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def get_stats() -> str:
    """Retourne les statistiques globales des événements collectés"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT source, COUNT(*) FROM events GROUP BY source")
    by_source = {r[0]: r[1] for r in cursor.fetchall()}
    cursor.execute("SELECT severity, COUNT(*) FROM events GROUP BY severity")
    by_severity = {r[0]: r[1] for r in cursor.fetchall()}
    conn.close()
    return json.dumps({"total_events": total, "by_source": by_source, "by_severity": by_severity}, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
