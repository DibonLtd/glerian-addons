# Development Guide - Partner Statement Branded

This guide is for developers who want to understand, extend, or customize the Partner Statement Branded module.

## Architecture Overview

```
Statement Generation Flow:

Partner Record
    ↓
    └─→ action_print_customer_statements()
        ↓
        └─→ _prepare_customer_statement_values()
            ├─→ _get_initial_balances()
            ├─→ _get_aml_values()
            └─→ Format & return data
        ↓
        └─→ Report Handler (CustomerStatementReport)
            ├─→ _get_report_values()
            └─→ _get_company_logo_b64()
        ↓
        └─→ QWeb Template (customer_statements_template.xml)
            └─→ Render PDF
        ↓
        └─→ Download/Print
```

## Key Components

### 1. Model Layer (`models/`)

#### `account_partner_ledger.py`
Extends `account.partner.ledger.report.handler` to:
- Hide specific columns from statements
- Customize display configuration
- Filter report data

**Key Method:**
```python
def _custom_options_initializer(self, report, options, previous_options=None):
    # Filters columns: journal, account, due_date, matching, amount_currency
```

**Extension Point:**
To add more column filtering, modify the `columns_to_hide` list:
```python
columns_to_hide = [
    'journal_id',
    'account_id',
    'date_maturity',
    'reconciliation_status',
    'amount_currency',
    'your_new_field',  # Add here
]
```

#### `res_partner.py`
Extends `res.partner` to:
- Add statement generation action
- Prepare statement data with branding
- Calculate running balances
- Query account move lines

**Key Methods:**
- `action_print_customer_statements()` - Main entry point
- `_prepare_customer_statement_values()` - Data preparation
- `_get_initial_balances()` - Balance calculations
- `_get_aml_values()` - Transaction data

**Extension Point:**
Add new methods for custom logic:
```python
def _calculate_custom_totals(self, options):
    """Your custom calculation"""
    for partner in self:
        # Your logic here
        pass
```

### 2. Report Layer (`report/`)

#### `customer_statements.py`
The report handler that:
- Retrieves company logo
- Prepares report context values
- Handles PDF generation

**Extension Point:**
```python
def _get_report_values(self, docids, data=None):
    """Add custom context here"""
    values = super()._get_report_values(docids, data)
    values['custom_data'] = self._get_custom_data()
    return values
```

#### `customer_statements_template.xml`
Main QWeb template with:
- Header with logo
- Customer information block
- Transaction table
- Company footer

**Extension Point:**
Add custom sections before `</template>`:
```xml
<div class="custom-section">
    <h3>Your Custom Content</h3>
    <t t-esc="custom_data" />
</div>
```

### 3. Styling Layer (`static/`)

#### `partner_ledger_branded.scss`
Main stylesheet with:
- Layout structure
- Color scheme
- Print styles
- Responsive design

**Customization:**
```scss
.partner_ledger_branded {
    // Override default colors
    --primary-color: #007bff;
    
    .statement-header {
        background: linear-gradient(to right, #f0f0f0, white);
    }
}
```

## Customization Examples

### Example 1: Add Age of Accounts Analysis

Add to `res_partner.py`:
```python
def _get_aging_analysis(self, options):
    """Calculate invoice aging"""
    from datetime import timedelta
    today = fields.Date.today()
    
    aging = {
        'current': 0,
        'overdue_30': 0,
        'overdue_60': 0,
        'overdue_90': 0,
    }
    
    amls = self._get_aml_values(options, None)
    for partner_id, lines in amls.items():
        for line in lines:
            date_maturity = line.get('date_maturity')
            if date_maturity:
                days_overdue = (today - date_maturity).days
                if days_overdue <= 0:
                    aging['current'] += line['balance']
                elif days_overdue <= 30:
                    aging['overdue_30'] += line['balance']
                # ... etc
    
    return aging
```

Then in `customer_statements_template.xml`, add:
```xml
<div class="aging-analysis">
    <h3>Account Aging</h3>
    <table>
        <tr>
            <td>Current:</td>
            <td t-esc="aging_data['current']" />
        </tr>
        <!-- ... -->
    </table>
</div>
```

### Example 2: Add Payment Terms Display

Modify `res_partner.py`:
```python
def _get_payment_terms_html(self):
    """Get formatted payment terms"""
    if self.property_payment_term_id:
        return self.property_payment_term_id.display_name
    return "Payment terms available upon request"
```

Add to template:
```xml
<div class="payment-terms">
    <p t-esc="payment_terms_html" />
</div>
```

### Example 3: Add Discounts/Credits Section

Create a new method:
```python
def _get_credits_applied(self, options):
    """Get list of credits and discounts"""
    credits = []
    for invoice in self.invoice_ids:
        if invoice.state == 'posted' and invoice.type == 'out_refund':
            credits.append({
                'number': invoice.name,
                'date': invoice.invoice_date,
                'amount': invoice.amount_total,
            })
    return credits
```

## Testing

### Unit Tests
Create `tests/test_partner_statement.py`:

```python
from odoo.tests.common import TransactionCase

class TestPartnerStatement(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@test.com',
        })
    
    def test_statement_generation(self):
        """Test statement can be generated"""
        result = self.partner.action_print_customer_statements()
        self.assertIsNotNone(result)
    
    def test_column_hiding(self):
        """Test that unwanted columns are hidden"""
        # Test logic here
        pass
```

Run tests:
```bash
odoo -i partner_statement_branded --test-enable --log-level=test
```

### Manual Testing Checklist
- [ ] Statement generates without errors
- [ ] Company logo appears
- [ ] Date range filtering works
- [ ] Running balance calculates correctly
- [ ] PDF downloads properly
- [ ] Multi-currency displays correctly
- [ ] Print layout looks good
- [ ] Footer text displays
- [ ] Long transaction lists paginate

## Performance Optimization

### 1. Optimize Database Queries

Instead of:
```python
for line in lines:
    line.move_id.journal_id.name  # N+1 query!
```

Use:
```python
lines = lines.with_context(prefetch_fields={'move_id': ['journal_id']})
```

### 2. Limit Statement Lines

Add pagination:
```python
def _get_aml_values(self, options, report, limit=100):
    """Get AML values with limit"""
    amls = self.env['account.move.line'].search(
        domain,
        order='move_id.date DESC',
        limit=limit,
    )
```

### 3. Cache Logo

Store logo in session:
```python
def _get_company_logo_b64(self):
    """Cache logo in context"""
    cache_key = 'company_logo_' + str(self.env.company.id)
    if cache_key not in self.env.context:
        # Generate and cache
        pass
```

## Common Issues & Solutions

### Issue: Columns Not Hidden
**Solution:** Ensure `_custom_options_initializer` runs after parent class. Use super():
```python
super()._custom_options_initializer(report, options, previous_options)
```

### Issue: Logo Not Showing
**Solution:** Verify image format and encoding:
```python
# Ensure PNG or JPG
if company.logo:
    # Check MIME type
    import imghdr
    img_type = imghdr.what(None, company.logo)
```

### Issue: Slow Statement Generation
**Solution:** Add SQL query optimization:
```python
# Bad: Multiple queries
for line in lines:
    line.move_id.partner_id.name

# Good: Use select_related equivalent
lines = lines.with_context(prefetch_fields={'move_id': ['partner_id']})
```

## Extending Report Columns

To add a new column visible in statements:

1. Add method to `res_partner.py`:
```python
def _get_invoice_count(self):
    return len(self.invoice_ids)
```

2. Add to template:
```xml
<th>Invoice Count</th>
<!-- In table body: -->
<td t-esc="doc._get_invoice_count()" />
```

3. Update SCSS for alignment:
```scss
th:nth-child(6) {
    width: 10%;
    text-align: center;
}
```

## Contributing Changes

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Keep changes focused
   - Follow Odoo coding standards
   - Add docstrings

3. **Test Thoroughly**
   - Test with demo data
   - Test with large datasets
   - Test PDF generation
   - Test multi-company scenario

4. **Document Changes**
   - Update README.md if needed
   - Update docstrings
   - Add to CHANGELOG.md

## Debugging

### Enable Debug Logging

```python
import logging
_logger = logging.getLogger(__name__)

class YourClass(models.Model):
    def my_method(self):
        _logger.debug(f"Debug info: {self}")
        _logger.warning(f"Warning: {value}")
```

Run with debug logging:
```bash
odoo --log-level=debug
```

### Inspect Generated Data

Add to template:
```xml
<!-- Temporary debugging -->
<div style="display:none;">
    <t t-esc="repr(partner_lines)" />
</div>
```

### Test Report Generation in Shell

```python
# In Odoo shell:
from odoo.tests.common import TestCase

partner = env['res.partner'].browse(1)
result = partner.action_print_customer_statements()
print(result)

# Test data preparation
values = partner._prepare_customer_statement_values()
print(values)
```

## Version Management

Version format: `17.0.MAJOR.MINOR.PATCH`

- `17.0` - Odoo version
- `MAJOR` - Breaking changes
- `MINOR` - New features
- `PATCH` - Bug fixes

Update in `__manifest__.py`:
```python
"version": "17.0.1.0.0",  # Change this
```

## Module Dependencies

Current dependencies:
- `account_reports` - Base reporting
- `base` - Odoo core

To add dependency:
1. Add to __manifest__.py:
   ```python
   "depends": ["account_reports", "base", "new_module"],
   ```
2. Test installation order

## File Naming Conventions

- Python files: `snake_case.py`
- XML files: `descriptive_name.xml`
- SCSS files: `component_name.scss`
- Templates: Variables in `{{ }}` or `t-set`

## Resources

- **Odoo Documentation:** https://www.odoo.com/documentation/17.0/
- **QWeb Reference:** https://www.odoo.com/documentation/17.0/developer/reference/frontend/qweb.html
- **ORM Reference:** https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html

---

**Happy Developing!** 🚀
