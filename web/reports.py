from datetime import datetime, timezone
from io import BytesIO

from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportItem(BaseModel):
    tool: str = Field(min_length=1, max_length=80)
    target: str = Field(min_length=1, max_length=253)
    endpoint: str = Field(default="", max_length=160)
    ok: bool = False
    returncode: int = 0
    stdout: str = Field(default="", max_length=20000)
    stderr: str = Field(default="", max_length=8000)
    results: list[str] = Field(default_factory=list, max_length=200)
    captured_at: str = Field(default="", max_length=80)


class ReportRequest(BaseModel):
    title: str = Field(default="Informe OSINT LAB PRO", min_length=3, max_length=120)
    subject: str = Field(default="", max_length=253)
    items: list[ReportItem] = Field(min_length=1, max_length=25)


def build_report_text(report: ReportRequest) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    subject = report.subject.strip() or _infer_subject(report.items)
    lines = [
        report.title,
        "",
        f"Fecha de generacion: {generated_at}",
        f"Objetivo principal: {subject}",
        "",
        "Resumen ejecutivo",
        "Este informe consolida los resultados obtenidos mediante tecnicas OSINT pasivas y consultas automatizadas.",
        "La informacion debe interpretarse como indicios tecnicos, no como una atribucion definitiva de identidad.",
        "",
        "Alcance",
        "El analisis se limita a los resultados devueltos por las herramientas ejecutadas desde OSINT LAB PRO.",
        "No se han realizado acciones intrusivas ni pruebas de acceso contra sistemas de terceros.",
        "",
        "Resultados por herramienta",
    ]

    for index, item in enumerate(report.items, start=1):
        status = "Correcto" if item.ok else "Con incidencias"
        lines.extend(
            [
                "",
                f"{index}. {item.tool}",
                f"Objetivo consultado: {item.target}",
                f"Estado: {status} (codigo {item.returncode})",
            ]
        )

        extracted = _extract_findings(item)

        if extracted:
            lines.append("Hallazgos principales:")
            lines.extend(f"- {finding}" for finding in extracted)
        else:
            lines.append("Hallazgos principales: no se han detectado resultados relevantes en la salida disponible.")

        if item.stderr.strip():
            lines.append(f"Observaciones tecnicas: {item.stderr.strip()[:600]}")

    lines.extend(
        [
            "",
            "Interpretacion",
            "Los resultados positivos pueden indicar presencia del objetivo en servicios publicos o registros consultados.",
            "Antes de tomar decisiones operativas, conviene validar manualmente los enlaces, fechas y contexto de cada hallazgo.",
            "",
            "Recomendaciones",
            "- Verificar manualmente los perfiles o dominios relevantes.",
            "- Guardar evidencias con fecha, hora y fuente consultada.",
            "- Evitar conclusiones de identidad sin contrastar con fuentes adicionales.",
            "- Utilizar este informe solo sobre objetivos propios o con autorizacion expresa.",
            "",
            "Aviso legal",
            "Este documento se genera con fines de auditoria, investigacion autorizada y documentacion tecnica.",
            "El uso indebido de informacion publica puede vulnerar privacidad, terminos de servicio o normativa aplicable.",
        ]
    )

    return "\n".join(lines)


def build_report_pdf(report: ReportRequest) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title=report.title,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SmallMono",
            parent=styles["BodyText"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#263442"),
        )
    )
    story = []
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    subject = report.subject.strip() or _infer_subject(report.items)

    story.append(Paragraph(_escape(report.title), styles["Title"]))
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        Table(
            [
                ["Fecha", generated_at],
                ["Objetivo principal", subject],
                ["Numero de consultas", str(len(report.items))],
            ],
            colWidths=[4.2 * cm, 11.0 * cm],
        )
    )
    story[-1].setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#111820")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9fb0bf")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(Spacer(1, 0.45 * cm))

    _section(story, styles, "Resumen ejecutivo")
    story.append(
        Paragraph(
            "Este informe consolida resultados obtenidos mediante tecnicas OSINT pasivas y consultas automatizadas. "
            "La informacion debe interpretarse como indicios tecnicos y requiere validacion manual antes de cualquier decision.",
            styles["BodyText"],
        )
    )

    _section(story, styles, "Resultados")

    for index, item in enumerate(report.items, start=1):
        status = "Correcto" if item.ok else "Con incidencias"
        story.append(Paragraph(f"{index}. {_escape(item.tool)}", styles["Heading3"]))
        story.append(Paragraph(f"Objetivo consultado: {_escape(item.target)}", styles["BodyText"]))
        story.append(Paragraph(f"Estado: {status} (codigo {item.returncode})", styles["BodyText"]))
        findings = _extract_findings(item)

        if findings:
            for finding in findings[:30]:
                story.append(Paragraph(f"- {_escape(finding)}", styles["BodyText"]))
        else:
            story.append(Paragraph("No se han detectado resultados relevantes en la salida disponible.", styles["BodyText"]))

        if item.stderr.strip():
            story.append(Paragraph("Observaciones tecnicas:", styles["BodyText"]))
            story.append(Paragraph(_escape(item.stderr.strip()[:800]), styles["SmallMono"]))

        story.append(Spacer(1, 0.25 * cm))

    _section(story, styles, "Interpretacion y recomendaciones")
    for line in [
        "Los resultados positivos pueden indicar presencia del objetivo en servicios publicos o registros consultados.",
        "Verificar manualmente perfiles, dominios y enlaces relevantes antes de sacar conclusiones.",
        "Guardar evidencias con fecha, hora y fuente consultada.",
        "Utilizar este informe solo sobre objetivos propios o con autorizacion expresa.",
    ]:
        story.append(Paragraph(f"- {_escape(line)}", styles["BodyText"]))

    _section(story, styles, "Aviso legal")
    story.append(
        Paragraph(
            "Documento generado con fines de auditoria, investigacion autorizada y documentacion tecnica. "
            "El uso indebido de informacion publica puede vulnerar privacidad, terminos de servicio o normativa aplicable.",
            styles["BodyText"],
        )
    )

    doc.build(story)
    return buffer.getvalue()


def _section(story: list, styles, title: str) -> None:
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph(_escape(title), styles["Heading2"]))
    story.append(Spacer(1, 0.12 * cm))


def _infer_subject(items: list[ReportItem]) -> str:
    if not items:
        return "No especificado"
    return items[0].target


def _extract_findings(item: ReportItem) -> list[str]:
    findings = [entry.strip() for entry in item.results if entry.strip()]

    if findings:
        return findings[:40]

    for line in item.stdout.splitlines():
        clean = line.strip()

        if clean.startswith("[+]"):
            findings.append(clean)
        elif clean.startswith("[*]") and "checking" not in clean.lower():
            findings.append(clean)

    return findings[:40]


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
