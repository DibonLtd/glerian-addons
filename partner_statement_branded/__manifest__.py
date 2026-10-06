# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Partner Statement Branded - Customer Ledger",
    "version": "17.0.1.0.7",
    "author": "Custom Development",
    "description": """
Partner Statement with Branding
================================
This module provides branded customer partner ledger and statement reports with:
- Company logo integration
- Professional header and footer
- Selective column visibility (removes: Journal, Account Number, Due Date, Matching, Amount Currency)
- Downloadable statements directly from partner contact
- Clean, customer-facing presentation
    """,
    "category": "Accounting/Reporting",
    "depends": ["account_reports", "base"],
    "data": [
        "views/res_partner_views.xml",
        "report/partner_ledger_pdf_export.xml",
        "report/customer_statements_template.xml",
        "report/customer_statements_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "partner_statement_branded/static/src/components/**/*",
        ],
        "account_reports.assets_pdf_export": [
            "partner_statement_branded/static/src/scss/partner_ledger_pdf_export.scss",
        ],
        "web.report_assets_common": [
            "partner_statement_branded/static/src/css/customer_statement_report.css",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
}
