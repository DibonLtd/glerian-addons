from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Used to add new fields to the settings"""
    _inherit = "res.config.settings"

    customer_details = fields.Boolean(string="Customer Details",
                                      help="By Enabling the customer details"
                                           " in pos receipt",
                                      config_parameter="pos_receipt_extend_dibon.customer_details")
    customer_name = fields.Boolean(string="Customer Name",
                                   help="By Enabling the customer name "
                                        "in pos receipt",
                                   config_parameter="pos_receipt_extend_dibon.customer_name")
    customer_address = fields.Boolean(string="Customer Address",
                                      help="By Enabling the customer Address "
                                           "in pos receipt",
                                      config_parameter="pos_receipt_extend_dibon.customer_address")
    customer_mobile = fields.Boolean(string="Customer Mobile",
                                     help="By Enabling the customer mobile "
                                          "in pos receipt",
                                     config_parameter="pos_receipt_extend_dibon.customer_mobile")
    customer_phone = fields.Boolean(string="Customer Phone",
                                    help="By Enabling the customer phone "
                                         "in pos receipt",
                                    config_parameter="pos_receipt_extend_dibon.customer_phone")
    customer_email = fields.Boolean(string="Customer Email",
                                    help="By Enabling the customer email "
                                         "in pos receipt",
                                    config_parameter="pos_receipt_extend_dibon.customer_email")
    customer_vat = fields.Boolean(string="Customer Vat",
                                  help="By Enabling the customer vat details "
                                       "in pos receipt",
                                  config_parameter="pos_receipt_extend_dibon.customer_vat")
