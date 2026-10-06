# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models
from odoo.exceptions import UserError


class PartnerLedgerCustomHandler(models.AbstractModel):
    """Custom handler for Partner Ledger - handles column hiding for customer-facing statements"""
    _inherit = 'account.partner.ledger.report.handler'

    def _get_custom_display_config(self):
        """Override to customize the display configuration for branded statements"""
        config = super()._get_custom_display_config()
        css_classes = [config.get('css_custom_class', ''), 'partner_ledger_branded']
        config['css_custom_class'] = ' '.join(dict.fromkeys(cls for cls in css_classes if cls))
        config.setdefault('pdf_export', {})
        config['pdf_export']['company_information'] = 'partner_statement_branded.partner_ledger_pdf_export_company_information'
        return config

    def _custom_options_initializer(self, report, options, previous_options=None):
        """Hide unwanted columns from customer-facing statements"""
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        hide_labels = {
            'journal_code',
            'account_code',
            'date_maturity',
            'matching_number',
            'amount_currency',
        }
        if options.get('columns'):
            options['columns'] = [
                column for column in options['columns']
                if column.get('expression_label') not in hide_labels
            ]

    @api.model
    def action_print_customer_statements(self, options, params):
        """Print the customer statements for a specific customer with branding"""
        model, record_id = self.env['account.report']._get_model_info_from_id(params['line_id'])
        if model != 'res.partner':
            raise UserError(_("This option is only available for customers."))

        partner = self.env[model].browse(record_id)
        return partner.action_print_customer_statements(options)
