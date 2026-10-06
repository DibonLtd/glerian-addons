# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class ResPartner(models.Model):
    """Extended Partner model for branded customer statements"""
    _inherit = 'res.partner'

    statement_footer_text = fields.Text(
        string="Statement Footer",
        help="Custom footer text for printed customer statements"
    )

    def action_print_customer_statements(self, options=None):
        """Print branded customer statements with company logo and header/footer"""
        if not self:
            raise UserError(_("Please select at least one partner to print statements."))

        # Use partner's language for the report, default to user language if mixed
        partner_languages = self.mapped('lang')
        report_lang = partner_languages[0] if len(partner_languages) == 1 else self.env.user.lang

        report = self.env.ref('partner_statement_branded.customer_statements_report')

        return report.with_context(
            report_options=options,
            lang=report_lang,
        ).report_action(self)

    def _prepare_customer_statement_values(self, options=None):
        """Prepare statement values using the official partner-ledger flow."""
        def format_monetary(value):
            return self.env['account.report']._format_value(
                options=options,
                value=value,
                currency=self.env.company.currency_id,
                figure_type='monetary',
            )

        if not self:
            raise UserError(
                _("The Customer Statements cannot be printed without a partner set.")
            )

        if options:
            from_date = options.get("date", {}).get("date_from") or fields.Date.today().replace(day=1)
            to_date = options.get("date", {}).get("date_to") or fields.Date.today()
            unreconciled = options.get("unreconciled", False)
            report = self.env['account.report'].browse(options.get('report_id')) or self.env.ref('account_reports.partner_ledger_report')
        else:
            from_date = fields.Date.today().replace(day=1)
            to_date = fields.Date.today()
            unreconciled = False
            report = self.env.ref('account_reports.partner_ledger_report')

        options = report.get_options(
            previous_options={
                'date': {
                    'date_from': from_date,
                    'date_to': to_date,
                    'mode': 'range',
                },
                'account_type': [
                    {'id': 'trade_receivable', 'selected': True},
                    {'id': 'non_trade_receivable', 'selected': False},
                    {'id': 'trade_payable', 'selected': False},
                    {'id': 'non_trade_payable', 'selected': False},
                ],
                'unreconciled': unreconciled,
                'multi_currency': True,
            }
        )

        initial_balances = self._get_initial_balances(options, report)
        line_values = self._get_aml_values(options, report)

        partner_lines = defaultdict(list)
        statement_summaries = {}
        partner_running_balances = defaultdict(float)

        for partner in self:
            opening_balance_raw = initial_balances[partner.id]
            partner_running_balances[partner.id] = opening_balance_raw

            partner_line_values = line_values.get(partner.id, [])
            period_movement_raw = sum(line_value.get('balance', 0.0) for line_value in partner_line_values)

            partner_lines[str(partner.id)].append({
                'date': format_date(self.env, from_date, date_format='d MMM yy'),
                'activity': _('Opening Balance'),
                'reference': '',
                'due_date': '',
                'amount': '',
                'amount_raw': 0.0,
                'move_type': '',
                'balance': format_monetary(opening_balance_raw),
                'balance_raw': opening_balance_raw,
                'line_kind': 'opening',
            })

            for line_value in partner_line_values:
                line_amount_raw = line_value.get('balance', 0.0)
                partner_running_balances[partner.id] += line_amount_raw
                is_payment = line_value.get('move_type') == 'entry' and line_value.get('payment_id')
                due_date = '' if is_payment else format_date(self.env, line_value.get('date_maturity'), date_format='d MMM yy')
                partner_lines[str(partner.id)].append({
                    'date': format_date(self.env, line_value.get('invoice_date') or line_value.get('date'), date_format='d MMM yy'),
                    'activity': line_value.get('move_name'),
                    'reference': line_value.get('ref'),
                    'due_date': due_date,
                    'amount': format_monetary(line_amount_raw),
                    'amount_raw': line_amount_raw,
                    'move_type': self._get_move_type(line_value),
                    'balance': format_monetary(partner_running_balances[partner.id]),
                    'balance_raw': partner_running_balances[partner.id],
                    'line_kind': 'payment' if is_payment else 'document',
                })

            statement_summaries[str(partner.id)] = {
                'opening_balance': format_monetary(opening_balance_raw),
                'opening_balance_raw': opening_balance_raw,
                'period_movement': format_monetary(period_movement_raw),
                'period_movement_raw': period_movement_raw,
                'balance_due': format_monetary(partner_running_balances[partner.id]),
                'balance_due_raw': partner_running_balances[partner.id],
                'transaction_count': len(partner_line_values),
            }

        return {
            'from_date': format_date(self.env, from_date, date_format='d MMMM yyyy').upper(),
            'to_date': format_date(self.env, to_date, date_format='d MMMM yyyy').upper(),
            'lines': partner_lines,
            'partner_lines': partner_lines,
            'statement_summaries': statement_summaries,
            'balances_due': {
                str(partner.id): format_monetary(partner_running_balances[partner.id]) for partner in self
            },
            'vat_label': {partner.id: partner.country_id.vat_label or 'VAT' for partner in self},
        }

    def _get_initial_balances(self, options, report):
        balances = self.env[report.custom_handler_model_name]._get_initial_balance_values(
            self.ids,
            options=options,
        )
        return {partner.id: next(iter(balances[partner.id].values())).get('balance', 0.0) for partner in self}

    def _get_aml_values(self, options, report):
        aml_values = self.env[report.custom_handler_model_name]._get_aml_values(
            options=options,
            partner_ids=self.ids,
        )
        return {partner.id: aml_values.get(partner.id, []) for partner in self}

    def _get_move_type(self, line_value):
        type_name_mapping = dict(
            self.env['account.move']._fields['move_type']._description_selection(self.env),
            out_invoice=_('Invoice'),
            out_refund=_('Credit Note'),
        )
        is_payment = line_value.get('move_type') == 'entry' and line_value.get('payment_id')
        move_type = type_name_mapping.get(line_value.get('move_type'), '')
        if is_payment:
            move_type = f"{'⬅' if line_value.get('balance', 0.0) < 0 else '➡'}{_('Payment')}"
        return move_type
