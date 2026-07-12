{
    "name": "AssetFlow",
    "summary": "Enterprise Asset & Resource Management System",
    "description": """
        AssetFlow is a production-ready Enterprise Asset & Resource Management System.
        Includes Organization, Asset Registration/Lifecycle, Asset Allocation, Resource Booking,
        Maintenance, Audit and Dashboard functionalities.
    """,
    "author": "Antigravity",
    "website": "https://www.yourcompany.com",
    "category": "Asset Management",
    "version": "1.0",
    "depends": ["base", "hr", "mail"],

    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        # "data/cron.xml",
        # "report/asset_report.xml",
        "views/department.xml",
        "views/asset_category.xml",
        "views/asset_views.xml",
        "views/assest_history_views.xml",
        "views/asset_allocation.xml",
        # "views/booking_views.xml",
        # "views/maintenance_views.xml",
        # "views/audit_views.xml",
        "views/audit_cycle_views.xml",
        "views/audit_line_views.xml",
        "views/dashboard_views.xml",
        "views/employee_views.xml",
        # "views/notification_views.xml",
        "views/transfer_views.xml",
    ],
    "installable": True,
    "application": True,
    "sequence": 1,
}
