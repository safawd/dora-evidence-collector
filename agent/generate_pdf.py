import markdown2
import os
from datetime import datetime

def generate_dora_pdf():
    report_md_path = "/root/DORA-PFE/agent/dora_report.md"
    report_pdf_path = "/root/DORA-PFE/agent/dora_report.pdf"
    report_html_path = "/root/DORA-PFE/agent/dora_report.html"

    # Lire le rapport Markdown
    with open(report_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convertir en HTML
    html_content = markdown2.markdown(
        md_content,
        extras=["tables", "fenced-code-blocks", "header-ids"]
    )

    # Template HTML professionnel
    html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport DORA</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            font-size: 12px;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .header {{
            background-color: #003366;
            color: white;
            padding: 30px 40px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: bold;
        }}
        .header p {{
            margin: 5px 0 0 0;
            font-size: 12px;
            opacity: 0.8;
        }}
        .content {{
            padding: 20px 40px;
        }}
        h1 {{ color: #003366; font-size: 20px; border-bottom: 2px solid #003366; padding-bottom: 5px; }}
        h2 {{ color: #003366; font-size: 16px; margin-top: 25px; }}
        h3 {{ color: #0055a4; font-size: 14px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th {{
            background-color: #003366;
            color: white;
            padding: 8px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .footer {{
            background-color: #f5f5f5;
            border-top: 2px solid #003366;
            padding: 15px 40px;
            font-size: 10px;
            color: #666;
            margin-top: 30px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .severity-critical {{ color: #cc0000; font-weight: bold; }}
        .severity-major {{ color: #ff6600; font-weight: bold; }}
        .severity-minor {{ color: #ffaa00; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 RAPPORT D'INCIDENT DORA</h1>
        <p>Digital Operational Resilience Act — EU Regulation 2022/2554</p>
        <p>Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
        <p>Système : Spring Boot Microservices Banking Application</p>
    </div>
    <div class="content">
        {html_content}
    </div>
    <div class="footer">
        <p>Document confidentiel — Rapport d'incident TIC conforme au règlement DORA (UE) 2022/2554</p>
        <p>Articles 17 (Gestion des incidents), 18 (Classification), 19 (Notification aux autorités)</p>
        <p>Généré automatiquement par le système DORA Evidence Collector</p>
    </div>
</body>
</html>"""

    # Sauvegarder le HTML
    with open(report_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ HTML généré : {report_html_path}")

    # Convertir en PDF avec weasyprint
    try:
      import pdfkit
      pdfkit.from_file(report_html_path, report_pdf_path)
      print(f"✅ PDF généré : {report_pdf_path}")
    except Exception as e:
      print(f"❌ Erreur PDF: {e}")
      print(f"💡 Le rapport HTML est disponible : {report_html_path}")

if __name__ == "__main__":
    generate_dora_pdf()
