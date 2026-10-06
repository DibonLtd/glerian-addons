# Partner Statement Branded Module

Professional customer-facing partner ledger and statement reports with company branding for Odoo 17.

## Features

### 🎨 Branding & Customization
- **Company Logo Integration**: Auto-displays company logo from res.company
- **Branded Header & Footer**: Professional statement headers with company information
- **Custom Footer Text**: Add custom footer text per partner for specific instructions
- **Professional Design**: Clean, modern layout optimized for PDF viewing

### 📊 Statement Management
- **Customer Statements Report**: Generate branded statements directly from partner contact
- **Downloadable Statements**: Print/download with a single click from partner record
- **Date Range Filtering**: Filter statements by date range (default: current month)
- **Running Balance Display**: Shows running account balance through statement period

### 🔍 Column Visibility Control
The module hides the following columns from customer-facing statements to reduce confusion:
- **Journal** - Internal accounting detail
- **Account Number** - System reference
- **Due Date** - Replaced with activity/invoice date in clean format
- **Matching** - Reconciliation status (internal use)
- **Amount Currency** - Multi-currency details (simplified to company currency)

Visible columns:
- Date (transaction date)
- Description/Activity (invoice, payment, etc.)
- Reference (document number)
- Amount (transaction amount)
- Balance (running balance)

## Module Structure

```
partner_statement_branded/
├── __manifest__.py                          # Module configuration
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── account_partner_ledger.py           # Partner ledger customization & column hiding
│   └── res_partner.py                       # Extended partner model with statement methods
├── report/
│   ├── __init__.py
│   ├── customer_statements.py              # Report handler with logo integration
│   ├── customer_statements_report.xml      # Report action definition
│   └── customer_statements_template.xml    # QWeb template with branding
├── data/
│   └── report_data.xml                     # Report configuration data
└── static/src/components/partner_ledger/
    └── partner_ledger_branded.scss         # Report styling
```

## Installation

1. Copy the `partner_statement_branded` folder to your Odoo addons directory:
   ```bash
   cp -r partner_statement_branded /path/to/odoo/addons/
   ```

2. Update your Odoo module list and install:
   - Navigate to Apps in Odoo
   - Click "Update Apps List"
   - Search for "Partner Statement Branded"
   - Click Install

## Usage

### Generating Customer Statements

**From Partner Contact:**
1. Open a partner/customer record
2. Click the "Print" button (or menu icon)
3. Select "Customer Statement" from the dropdown
4. Optionally set date range in the report options
5. Click "Print" or "Download"

**Programmatic Usage:**
```python
# From a partner record
partner = self.env['res.partner'].browse(partner_id)
options = {
    'date': {
        'date_from': '2024-01-01',
        'date_to': '2024-01-31',
    }
}
return partner.action_print_customer_statements(options)
```

### Customizing Partner Statements

**Add Custom Footer Text:**
1. Open a partner record
2. Find the "Statement Footer" field
3. Enter custom text (e.g., "Please submit payment within 30 days")
4. Save

The footer will appear on printed statements below company information.

## Technical Details

### Column Hiding Mechanism

The module extends `account.partner.ledger.report.handler` and implements:

```python
def _custom_options_initializer(self, report, options, previous_options=None):
    """Hide unwanted columns from customer-facing statements"""
```

This method filters out columns by expression_label matching:
- `journal` → Journal column hidden
- `account` → Account Number column hidden
- `due_date` → Due Date column hidden
- `matching` → Matching status hidden
- `amount_currency` → Currency details hidden

### Logo Integration

The report handler automatically retrieves company logo from `res.company.logo`:

```python
def _get_company_logo_b64(self):
    """Get company logo in base64 format"""
    company = self.env.company
    if company.logo:
        return company.logo.decode('utf-8') if isinstance(company.logo, bytes) else company.logo
```

The template then displays it in the statement header.

### Statement Data Preparation

The `_prepare_customer_statement_values()` method:
1. Gets initial account balance before the statement period
2. Collects all transactions in the date range
3. Calculates running balance through transactions
4. Formats dates and amounts for display

## Styling & Customization

### SCSS Variables & Classes

Main styling class: `.partner_ledger_branded`

Sub-classes:
- `.statement-header` - Top section with logo and dates
- `.company-logo` - Logo image styling
- `.statement-title` - Title and period display
- `.customer-info` - Customer address block
- `.statement-table` - Main transaction table
- `.statement-footer` - Company footer information
- `.payment-notice` - Payment terms notice at bottom

### Overriding Styles

Create your own SCSS file:
```scss
.partner_ledger_branded {
    /* Your customizations */
    .company-logo {
        max-width: 200px; /* Change logo size */
    }
    
    .statement-header {
        background-color: #f5f5f5; /* Add background */
    }
}
```

## API Reference

### ResPartner Methods

#### `action_print_customer_statements(options=None)`
Generate and return an action to print customer statements.

**Parameters:**
- `options` (dict, optional) - Report options including date range

**Returns:**
- Report action for printing/downloading

**Example:**
```python
partner.action_print_customer_statements({
    'date': {
        'date_from': '2024-01-01',
        'date_to': '2024-01-31',
    }
})
```

#### `_prepare_customer_statement_values(options=None)`
Prepare statement data with branding elements.

**Returns:**
- Dictionary with statement lines and formatting data

### Models

#### Models Extended
- `account.partner.ledger.report.handler` - Column hiding logic
- `res.partner` - Statement printing methods
- `ir.actions.report` - Custom report action

## Database Changes

### New Fields
- `res.partner.statement_footer_text` (Text field) - Custom footer for partner

### New Reports
- `report.partner_statement_branded.customer_statements` - Statement report

## Dependencies

- `account_reports` - Base reporting framework
- `base` - Core Odoo functionality

**Odoo Version:** 17.0

## Compatibility

- ✅ Odoo 17.0
- ✅ Multi-language support
- ✅ Multi-currency support (displays in company currency)
- ✅ PDF export
- ✅ Screen viewing

## Troubleshooting

### Statement shows all columns
**Solution:** Clear browser cache and refresh. Ensure module is properly installed.

### Logo not appearing in statement
**Solution:** 
1. Ensure company logo is set (Settings → Company Logo)
2. Check that the image format is supported (PNG, JPG)
3. Clear cache and regenerate statement

### Date range not filtering
**Solution:** 
1. Check that date fields are in YYYY-MM-DD format
2. Verify there are transactions in the selected date range
3. Check account type filters (defaults to Receivables)

### Statement page breaking issues
**Solution:** 
1. In Settings, try different page formats
2. Reduce font size in SCSS if needed
3. Test PDF generation (not screen preview)

## Contributing

For bug reports, feature requests, or contributions, please:
1. Test thoroughly in a development environment
2. Document changes clearly
3. Follow Odoo coding standards
4. Submit changes with detailed description

## License

AGPL-3.0 (See LICENSE file for details)

## Author

Custom Development

## Support

For support or customization requests, contact your Odoo administrator or system integrator.

---

**Last Updated:** March 23, 2026

**Version:** 17.0.1.0.0
