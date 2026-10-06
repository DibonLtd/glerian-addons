# Changelog

All notable changes to the Partner Statement Branded module will be documented in this file.

## [17.0.1.0.0] - 2024-03-23

### Initial Release

#### Added
- **Core Features**
  - Customer statement generation with company branding
  - Download functionality from partner contact
  - Branded header with company logo
  - Professional footer with company information
  - Custom footer text field per partner
  - Date range filtering (default: current month)

- **Column Management**
  - Hide Journal column
  - Hide Account Number column
  - Hide Due Date column
  - Hide Matching status column
  - Hide Amount Currency column
  - Keep visible: Date, Description, Reference, Amount, Balance

- **Models**
  - Extended `account.partner.ledger.report.handler` for column filtering
  - Extended `res.partner` with statement methods and fields
  - Custom statement report handler with logo integration

- **Reports**
  - Customer Statement PDF report
  - Branded template with professional layout
  - Running balance calculation
  - Multi-partner batch processing

- **UI/Styling**
  - Professional SCSS styling
  - Print-optimized layout
  - Responsive design
  - Company branding integration

- **Documentation**
  - README.md with full feature documentation
  - INSTALLATION_GUIDE.md with step-by-step setup
  - DEVELOPMENT.md for developers
  - Inline code documentation

#### Technical Details
- Odoo Version: 17.0
- Python 3.8+
- Uses QWeb templating engine
- PostgreSQL 12+
- License: AGPL-3.0

#### Database Changes
- New field: `res.partner.statement_footer_text` (Text)

#### Dependencies
- account_reports
- base

#### Breaking Changes
- None (initial release)

#### Known Issues
- None identified

#### Testing
- Manual testing completed for:
  - Statement generation
  - PDF export
  - Column visibility
  - Logo integration
  - Footer text display
  - Date filtering
  - Multi-company scenarios

### Files in This Release

```
partner_statement_branded/
├── __init__.py
├── __manifest__.py
├── README.md
├── INSTALLATION_GUIDE.md
├── DEVELOPMENT.md
├── CHANGELOG.md
├── LICENSE
├── models/
│   ├── __init__.py
│   ├── account_partner_ledger.py
│   └── res_partner.py
├── report/
│   ├── __init__.py
│   ├── customer_statements.py
│   ├── customer_statements_report.xml
│   └── customer_statements_template.xml
├── data/
│   └── report_data.xml
└── static/src/components/partner_ledger/
    └── partner_ledger_branded.scss
```

---

## Future Roadmap

### Planned for v17.0.2.0.0
- [ ] Email statement functionality
- [ ] Scheduled statement sending
- [ ] Statement history/archive
- [ ] Payment method display
- [ ] Activity notes integration

### Planned for v17.0.3.0.0
- [ ] Customer portal access to statements
- [ ] Multi-language statement headers
- [ ] Aging analysis section
- [ ] Custom branding per customer
- [ ] Statement signature blocks

### Planned for v17.1.0.0.0
- [ ] Odoo 18 compatibility
- [ ] Advanced filtering options
- [ ] Statement templates
- [ ] Batch processing API
- [ ] Webhook integrations

---

## Notes for Users

### v17.0.1.0.0 - Tips & Best Practices

1. **Setup Guide**
   - Configure company logo in Settings before printing first statement
   - Add custom footer text in partner record for consistent messaging
   - Test statement with a few partners before rolling out broadly

2. **Best Practices**
   - Use consistent date ranges monthly (e.g., 1st to last day of month)
   - Add footer text for payment terms and contact instructions
   - Review PDF output before sending to customers
   - Archive statements in customer portal (future release)

3. **Performance Notes**
   - Statements with 100+ transactions may take longer to generate
   - PDF caching enabled by default (set attachment_use=True)
   - First statement generation slightly slower due to logo processing

### Migration Notes
- No migration needed - this is initial release
- Compatible with existing partner records immediately upon installation

---

## Version Numbering Scheme

Using Semantic Versioning: `MAJOR.MINOR.PATCH`

With Odoo version prefix: `17.0.MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes that require code updates
- **MINOR**: New features maintaining backward compatibility
- **PATCH**: Bug fixes and security patches
- **Odoo version**: First part matches Odoo major version

---

## Support & Bug Reports

To report bugs or request features:
1. Document the exact steps to reproduce
2. Include Odoo version and module version
3. Attach sample data if possible
4. Note any error messages or logs

---

## Contributors

### v17.0.1.0.0
- Custom Development Team

---

**Last Updated:** March 23, 2024

**Current Version:** 17.0.1.0.0

**Status:** Stable / Production Ready ✅
