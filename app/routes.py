from flask import jsonify, request, render_template

from config.database import get_database_connection

from utils.incident_repository import (
    get_all_incidents,
    get_incident_summary,
    get_incident_summary_by_area,
    get_incident_statistics,
    create_incident,
    get_incidents_by_status,
    get_incident_by_id,
    resolve_incident
)

from monitoring.alert_repository import (
    get_all_alerts,
    get_alert_by_id,
    get_alerts_by_severity
)

from monitoring.incident_store import get_local_open_incidents
from monitoring.health_monitor import run_full_health_check


def register_routes(app):

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "UP",
            "message": "Application is healthy"
        }), 200

    @app.route("/customers", methods=["GET"])
    def get_customers():

        connection = None
        cursor = None

        try:
            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT
                    customer_id,
                    name,
                    email,
                    created_at
                FROM customers
                ORDER BY customer_id
            """)

            customers = cursor.fetchall()

            for customer in customers:
                if customer["created_at"] is not None:
                    customer["created_at"] = (
                        customer["created_at"].isoformat()
                    )

            return jsonify({
                "count": len(customers),
                "customers": customers
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve customers"
            }), 500

        finally:
            if cursor is not None:
                cursor.close()

            if (
                connection is not None
                and connection.is_connected()
            ):
                connection.close()

    @app.route("/orders", methods=["GET"])
    def get_orders():

        connection = None
        cursor = None

        try:
            status = request.args.get("status")
            customer_id = request.args.get("customer_id")

            page = request.args.get("page", "1")
            limit = request.args.get("limit", "50")

            valid_statuses = {
                "PENDING",
                "COMPLETED",
                "CANCELLED"
            }

            if status is not None:
                status = status.upper()

                if status not in valid_statuses:
                    return jsonify({
                        "status": "ERROR",
                        "message": (
                            "Invalid status. Use PENDING, "
                            "COMPLETED, or CANCELLED."
                        )
                    }), 400

            if customer_id is not None:
                try:
                    customer_id = int(customer_id)
                except ValueError:
                    return jsonify({
                        "status": "ERROR",
                        "message": "customer_id must be an integer."
                    }), 400

                if customer_id <= 0:
                    return jsonify({
                        "status": "ERROR",
                        "message": "customer_id must be greater than 0."
                    }), 400

            try:
                page = int(page)
                limit = int(limit)
            except ValueError:
                return jsonify({
                    "status": "ERROR",
                    "message": "page and limit must be integers."
                }), 400

            if page <= 0:
                return jsonify({
                    "status": "ERROR",
                    "message": "page must be greater than 0."
                }), 400

            if limit <= 0:
                return jsonify({
                    "status": "ERROR",
                    "message": "limit must be greater than 0."
                }), 400

            if limit > 100:
                return jsonify({
                    "status": "ERROR",
                    "message": "limit cannot be greater than 100."
                }), 400

            offset = (page - 1) * limit

            base_query = """
                FROM orders AS o
                INNER JOIN customers AS c
                    ON o.customer_id = c.customer_id
            """

            conditions = []
            parameters = []

            if status is not None:
                conditions.append("o.status = %s")
                parameters.append(status)

            if customer_id is not None:
                conditions.append("o.customer_id = %s")
                parameters.append(customer_id)

            where_clause = ""

            if conditions:
                where_clause = (
                    " WHERE " + " AND ".join(conditions)
                )

            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            count_query = """
                SELECT COUNT(*) AS total
            """ + base_query + where_clause

            cursor.execute(
                count_query,
                parameters
            )

            total = cursor.fetchone()["total"]

            orders_query = """
                SELECT
                    o.order_id,
                    o.customer_id,
                    c.name AS customer_name,
                    c.email AS customer_email,
                    o.product,
                    o.amount,
                    o.status,
                    o.created_at
            """ + base_query + where_clause + """
                ORDER BY o.order_id
                LIMIT %s OFFSET %s
            """

            order_parameters = parameters + [
                limit,
                offset
            ]

            cursor.execute(
                orders_query,
                order_parameters
            )

            orders = cursor.fetchall()

            for order in orders:
                if order["created_at"] is not None:
                    order["created_at"] = (
                        order["created_at"].isoformat()
                    )

            total_pages = (total + limit - 1) // limit

            return jsonify({
                "page": page,
                "limit": limit,
                "count": len(orders),
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
                "orders": orders
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve orders"
            }), 500

        finally:
            if cursor is not None:
                cursor.close()

            if (
                connection is not None
                and connection.is_connected()
            ):
                connection.close()

    @app.route("/incidents", methods=["GET"])
    def get_incidents():

        status = request.args.get(
            "status",
            "OPEN"
        ).upper()

        severity = request.args.get("severity")

        if severity is not None:
            severity = severity.upper()

        area = request.args.get("area")

        if area is not None:
            area = area.upper()

        valid_statuses = {
            "OPEN",
            "RESOLVED"
        }

        valid_severities = {
            "WARNING",
            "CRITICAL"
        }

        valid_areas = {
            "APPLICATION",
            "DATABASE",
            "TEST"
        }

        if status not in valid_statuses:
            return jsonify({
                "status": "ERROR",
                "message": (
                    "Invalid incident status. "
                    "Use OPEN or RESOLVED."
                )
            }), 400

        if (
            severity is not None
            and severity not in valid_severities
        ):
            return jsonify({
                "status": "ERROR",
                "message": (
                    "Invalid incident severity. "
                    "Use WARNING or CRITICAL."
                )
            }), 400

        if (
            area is not None
            and area not in valid_areas
        ):
            return jsonify({
                "status": "ERROR",
                "message": (
                    "Invalid incident area. "
                    "Use APPLICATION, DATABASE, or TEST."
                )
            }), 400

        try:
            incidents = get_incidents_by_status(
                status,
                severity,
                area
            )

            for incident in incidents:

                if incident["detected_at"] is not None:
                    incident["detected_at"] = (
                        incident["detected_at"].isoformat()
                    )

                if incident["resolved_at"] is not None:
                    incident["resolved_at"] = (
                        incident["resolved_at"].isoformat()
                    )

            return jsonify({
                "count": len(incidents),
                "source": "MYSQL",
                "incidents": incidents
            }), 200

        except Exception:

            if status == "OPEN":

                local_incidents = get_local_open_incidents()

                return jsonify({
                    "count": len(local_incidents),
                    "source": "LOCAL_FALLBACK",
                    "incidents": local_incidents
                }), 200

            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incidents"
            }), 500

    @app.route("/incidents/summary", methods=["GET"])
    def get_incident_summary_api():

        try:
            summary = get_incident_summary()

            return jsonify({
                "total": summary["total"],
                "open": summary["open"],
                "resolved": summary["resolved"],
                "critical": summary["critical"],
                "warning": summary["warning"]
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incident summary"
            }), 500

    @app.route("/incidents/summary/areas", methods=["GET"])
    def get_incident_summary_by_area_api():

        try:
            summaries = get_incident_summary_by_area()

            for summary in summaries:
                summary["total"] = int(summary["total"])
                summary["open"] = int(summary["open"])
                summary["resolved"] = int(summary["resolved"])

            return jsonify({
                "areas": summaries
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incident area summary"
            }), 500

    @app.route("/incidents/statistics", methods=["GET"])
    def get_incident_statistics_api():

        try:
            statistics = get_incident_statistics()

            for statistic in statistics:
                statistic["total"] = int(statistic["total"])
                statistic["open"] = int(statistic["open"])
                statistic["resolved"] = int(statistic["resolved"])

            return jsonify({
                "statistics": statistics
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incident statistics"
            }), 500

    @app.route("/incidents/history", methods=["GET"])
    def get_incident_history():

        try:
            incidents = get_all_incidents()

            for incident in incidents:

                if incident["detected_at"] is not None:
                    incident["detected_at"] = (
                        incident["detected_at"].isoformat()
                    )

                if incident["resolved_at"] is not None:
                    incident["resolved_at"] = (
                        incident["resolved_at"].isoformat()
                    )

            return jsonify({
                "count": len(incidents),
                "source": "MYSQL",
                "incidents": incidents
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incident history"
            }), 500

    @app.route(
        "/incidents/<int:incident_id>",
        methods=["GET"]
    )
    def get_incident_details(incident_id):

        try:
            incident = get_incident_by_id(incident_id)

            if incident is None:
                return jsonify({
                    "status": "ERROR",
                    "message": "Incident not found"
                }), 404

            if incident["detected_at"] is not None:
                incident["detected_at"] = (
                    incident["detected_at"].isoformat()
                )

            if incident["resolved_at"] is not None:
                incident["resolved_at"] = (
                    incident["resolved_at"].isoformat()
                )

            return jsonify({
                "incident": incident
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve incident"
            }), 500

    @app.route(
        "/incidents/<int:incident_id>/resolve",
        methods=["PATCH"]
    )
    def resolve_incident_api(incident_id):

        try:
            updated = resolve_incident(incident_id)

            if updated == 0:
                return jsonify({
                    "status": "ERROR",
                    "message": "Open incident not found"
                }), 404

            return jsonify({
                "status": "RESOLVED",
                "message": "Incident resolved successfully",
                "incident_id": incident_id
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to resolve incident"
            }), 500

    @app.route(
        "/incidents",
        methods=["POST"]
    )
    def create_incident_api():

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "status": "ERROR",
                "message": "Request body is required"
            }), 400

        required_fields = [
            "severity",
            "area",
            "root_cause",
            "recommended_action"
        ]

        missing_fields = [
            field
            for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return jsonify({
                "status": "ERROR",
                "message": "Missing required fields",
                "fields": missing_fields
            }), 400

        severity = data["severity"].upper()
        area = data["area"].upper()

        valid_severities = {
            "WARNING",
            "CRITICAL"
        }

        if severity not in valid_severities:
            return jsonify({
                "status": "ERROR",
                "message": "Severity must be WARNING or CRITICAL"
            }), 400

        try:
            incident_id = create_incident(
                severity=severity,
                area=area,
                root_cause=data["root_cause"],
                recommended_action=data["recommended_action"]
            )

            incident = get_incident_by_id(incident_id)

            if incident is None:
                return jsonify({
                    "status": "ERROR",
                    "message": (
                        "Incident was created but "
                        "could not be retrieved"
                    )
                }), 500

            if incident["detected_at"] is not None:
                incident["detected_at"] = (
                    incident["detected_at"].isoformat()
                )

            if incident["resolved_at"] is not None:
                incident["resolved_at"] = (
                    incident["resolved_at"].isoformat()
                )

            return jsonify({
                "status": "OPEN",
                "message": "Incident created successfully",
                "incident_id": incident_id,
                "incident": incident
            }), 201

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to create incident"
            }), 500

    # ---------------------------------------------------------
    # ALERT APIs
    # ---------------------------------------------------------

    @app.route("/alerts", methods=["GET"])
    def get_alerts_api():

        severity = request.args.get("severity")

        if severity is not None:
            severity = severity.upper()

        valid_severities = {
            "WARNING",
            "CRITICAL"
        }

        if (
            severity is not None
            and severity not in valid_severities
        ):
            return jsonify({
                "status": "ERROR",
                "message": (
                    "Invalid alert severity. "
                    "Use WARNING or CRITICAL."
                )
            }), 400

        try:

            if severity is None:
                alerts = get_all_alerts()
            else:
                alerts = get_alerts_by_severity(
                    severity
                )

            for alert in alerts:

                if alert["created_at"] is not None:
                    alert["created_at"] = (
                        alert["created_at"].isoformat()
                    )

            return jsonify({
                "count": len(alerts),
                "alerts": alerts
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve alerts"
            }), 500

    @app.route(
        "/alerts/<int:alert_id>",
        methods=["GET"]
    )
    def get_alert_details(alert_id):

        try:

            alert = get_alert_by_id(alert_id)

            if alert is None:
                return jsonify({
                    "status": "ERROR",
                    "message": "Alert not found"
                }), 404

            if alert["created_at"] is not None:
                alert["created_at"] = (
                    alert["created_at"].isoformat()
                )

            return jsonify({
                "alert": alert
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to retrieve alert"
            }), 500

    # ---------------------------------------------------------
    # DASHBOARD API
    # ---------------------------------------------------------

    @app.route("/dashboard", methods=["GET"])
    def dashboard():

        try:
            health_report = run_full_health_check()

            api_results = health_report["api"]

            failed_endpoints = [
                result["endpoint"]
                for result in api_results
                if not result["status_ok"]
            ]

            slow_endpoints = [
                result["endpoint"]
                for result in api_results
                if (
                    result["status_ok"]
                    and not result["response_time_ok"]
                )
            ]

            if failed_endpoints:
                api_status = "DOWN"
            elif slow_endpoints:
                api_status = "DEGRADED"
            else:
                api_status = "UP"

            database_result = health_report["database"]

            summary = get_incident_summary()

            recent_incidents = get_incidents_by_status(
                "OPEN"
            )[:5]

            for incident in recent_incidents:

                if incident["detected_at"] is not None:
                    incident["detected_at"] = (
                        incident["detected_at"].isoformat()
                    )

                if incident["resolved_at"] is not None:
                    incident["resolved_at"] = (
                        incident["resolved_at"].isoformat()
                    )

            return jsonify({
                "system_status": health_report["overall_status"],
                "api": {
                    "status": api_status,
                    "total_endpoints": len(api_results),
                    "healthy_endpoints": (
                        len(api_results)
                        - len(failed_endpoints)
                    ),
                    "slow_endpoints": len(slow_endpoints),
                    "failed_endpoints": len(failed_endpoints),
                    "failed_endpoint_names": failed_endpoints,
                    "slow_endpoint_names": slow_endpoints
                },
                "database": {
                    "status": database_result["status"],
                    "response_time": database_result["response_time"],
                    "query_ok": database_result["query_ok"],
                    "response_time_ok": (
                        database_result["response_time_ok"]
                    )
                },
                "incidents": {
                    "total": int(summary["total"] or 0),
                    "open": int(summary["open"] or 0),
                    "resolved": int(summary["resolved"] or 0),
                    "critical": int(summary["critical"] or 0),
                    "warning": int(summary["warning"] or 0)
                },
                "recent_incidents": recent_incidents
            }), 200

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": (
                    "Unable to retrieve dashboard information"
                )
            }), 500

    @app.route("/dashboard/view", methods=["GET"])
    def dashboard_view():

        try:
            health_report = run_full_health_check()

            api_results = health_report["api"]

            failed_endpoints = [
                result["endpoint"]
                for result in api_results
                if not result["status_ok"]
            ]

            slow_endpoints = [
                result["endpoint"]
                for result in api_results
                if (
                    result["status_ok"]
                    and not result["response_time_ok"]
                )
            ]

            if failed_endpoints:
                api_status = "DOWN"
            elif slow_endpoints:
                api_status = "DEGRADED"
            else:
                api_status = "UP"

            database_result = health_report["database"]

            summary = get_incident_summary()

            recent_incidents = get_incidents_by_status(
                "OPEN"
            )[:5]

            for incident in recent_incidents:

                if incident["detected_at"] is not None:
                    incident["detected_at"] = (
                        incident["detected_at"].isoformat()
                    )

                if incident["resolved_at"] is not None:
                    incident["resolved_at"] = (
                        incident["resolved_at"].isoformat()
                    )

            dashboard_data = {
                "system_status": health_report["overall_status"],
                "api": {
                    "status": api_status,
                    "total_endpoints": len(api_results),
                    "healthy_endpoints": (
                        len(api_results)
                        - len(failed_endpoints)
                    ),
                    "slow_endpoints": len(slow_endpoints),
                    "failed_endpoints": len(failed_endpoints),
                    "failed_endpoint_names": failed_endpoints,
                    "slow_endpoint_names": slow_endpoints
                },
                "database": {
                    "status": database_result["status"],
                    "response_time": database_result["response_time"],
                    "query_ok": database_result["query_ok"],
                    "response_time_ok": (
                        database_result["response_time_ok"]
                    )
                },
                "incidents": {
                    "total": int(summary["total"] or 0),
                    "open": int(summary["open"] or 0),
                    "resolved": int(summary["resolved"] or 0),
                    "critical": int(summary["critical"] or 0),
                    "warning": int(summary["warning"] or 0)
                },
                "recent_incidents": recent_incidents
            }

            return render_template(
                "dashboard.html",
                dashboard=dashboard_data
            )

        except Exception:
            return jsonify({
                "status": "ERROR",
                "message": "Unable to load dashboard"
            }), 500