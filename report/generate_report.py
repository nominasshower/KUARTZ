"""Genera report/data.json con metricas de Google Analytics (GA4) para Kuartz.
Requiere la variable de entorno GOOGLE_APPLICATION_CREDENTIALS apuntando a la
clave de la cuenta de servicio con rol Lector en la propiedad GA4.
"""
import json
import os
import sys
from datetime import datetime, timezone

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric, OrderBy,
    FilterExpression, Filter,
)

PROPERTY = "properties/547800341"


def event_filter(event_name):
    return FilterExpression(
        filter=Filter(
            field_name="eventName",
            string_filter=Filter.StringFilter(value=event_name),
        )
    )


def run(dimensions, metrics, order_by=None, limit=None, date_range="30daysAgo", dimension_filter=None):
    client = BetaAnalyticsDataClient()
    req = RunReportRequest(
        property=PROPERTY,
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=date_range, end_date="today")],
        order_bys=order_by or [],
        limit=limit,
        dimension_filter=dimension_filter,
    )
    resp = client.run_report(req)
    rows = []
    for row in resp.rows:
        rows.append({
            "dims": [v.value for v in row.dimension_values],
            "metrics": [v.value for v in row.metric_values],
        })
    return rows


def main():
    out = {"generated_at": datetime.now(timezone.utc).isoformat()}

    # Trafico diario ultimos 30 dias
    daily = run(
        ["date"], ["sessions", "activeUsers", "screenPageViews"],
        order_by=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
    )
    out["daily"] = [
        {"date": r["dims"][0], "sessions": int(r["metrics"][0]),
         "users": int(r["metrics"][1]), "pageviews": int(r["metrics"][2])}
        for r in daily
    ]

    # Totales del periodo
    totals = run([], ["sessions", "activeUsers", "screenPageViews"])
    if totals:
        out["totals"] = {
            "sessions": int(totals[0]["metrics"][0]),
            "users": int(totals[0]["metrics"][1]),
            "pageviews": int(totals[0]["metrics"][2]),
        }
    else:
        out["totals"] = {"sessions": 0, "users": 0, "pageviews": 0}

    # Que aplicacion ven mas (Kitchen/Vanity/Walls)
    apps = run(
        ["customEvent:application_type"], ["eventCount"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
        dimension_filter=event_filter("view_application"),
    )
    out["applications"] = [
        {"name": r["dims"][0], "count": int(r["metrics"][0])}
        for r in apps if r["dims"][0] and r["dims"][0] != "(not set)"
    ]

    # Que color ven mas en Colecciones
    colors = run(
        ["customEvent:color_name"], ["eventCount"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
        limit=15,
        dimension_filter=event_filter("view_color"),
    )
    out["colors_viewed"] = [
        {"name": r["dims"][0], "count": int(r["metrics"][0])}
        for r in colors if r["dims"][0] and r["dims"][0] != "(not set)"
    ]

    # Que color piden en las cotizaciones (el dato mas valioso)
    leads = run(
        ["customEvent:color_of_interest"], ["eventCount"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
        dimension_filter=event_filter("generate_lead"),
    )
    out["leads_by_color"] = [
        {"name": r["dims"][0] or "(sin especificar)", "count": int(r["metrics"][0])}
        for r in leads
    ]
    out["total_leads"] = sum(l["count"] for l in out["leads_by_color"])

    # Descargas de catalogo
    cat = run(["eventName"], ["eventCount"])
    cat_map = {r["dims"][0]: int(r["metrics"][0]) for r in cat}
    out["downloads_catalog"] = cat_map.get("download_catalog", 0)
    out["quote_form_submits"] = cat_map.get("generate_lead", 0)


    # Paises de los visitantes
    countries = run(
        ["country"], ["activeUsers"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="activeUsers"), desc=True)],
        limit=10,
    )
    out["countries"] = [
        {"name": r["dims"][0], "users": int(r["metrics"][0])}
        for r in countries
    ]

    dest = os.path.join(os.path.dirname(__file__), "data.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"OK: {dest}")
    print(json.dumps(out, ensure_ascii=False, indent=2)[:2000])


if __name__ == "__main__":
    main()
