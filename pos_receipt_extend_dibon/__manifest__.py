{
    'name': "Customer Details-POS Receipt",
    "version": "17.0.1.0.1",
    "category": "Point of Sale",
    "summary": "Advanced POS Receipt with Customer Details and Invoice Details "
               "will Allow You to Print The Customer Information in the pos receipt",
    "description": """Advanced POS Receipt with Customer Details and Invoice Details""",
    'author': 'Gasine Mwangi',
    'website': "https://www.dibon.co.ke",
    'company': 'Dibon Ltd',
    'maintainer': 'Dibon Ltd',
    'depends': ['point_of_sale', 'sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_receipt_extend_dibon/static/src/xml/OrderReceipt.xml',
            'pos_receipt_extend_dibon/static/src/js/pos_order_receipt.js',
            'pos_receipt_extend_dibon/static/src/js/payment.js',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
