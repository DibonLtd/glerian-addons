from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    report = env.ref(
        'partner_statement_branded.customer_statements_report',
        raise_if_not_found=False,
    )
    if report:
        report.write({
            'print_report_name': "'Customer_Statement_%s_%s' % ((object.display_name or 'partner').replace('/', '-'), time.strftime('%Y%m%d'))",
            'report_name': 'partner_statement_branded.customer_statements',
            'report_file': 'partner_statement_branded.customer_statements',
        })
