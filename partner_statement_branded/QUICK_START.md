# 🚀 Quick Start - Partner Statement Branded

Get your branded customer statements running in **3 simple steps**.

## Step 1️⃣: Install Module (1 minute)

```bash
# Module is ready at:
/home/rock/Desktop/2026_Projects/ODOO/Builds/random_odoo_modules/partner_statement_branded/
```

In Odoo:
1. **Apps** → Search: "Partner Statement"
2. Click **Install**
3. Wait for completion ✅

## Step 2️⃣: Upload Company Logo (1 minute)

1. **Settings** → **Companies** → Select your company
2. Upload a logo image
3. Save ✅

## Step 3️⃣: Generate Your First Statement (1 minute)

1. **Contacts** → Pick any customer
2. Click **Print** button (⋮ menu)
3. Select **Customer Statement**
4. Click **Print** or **Download** ✅

**Done!** Your branded statement is ready. 🎉

---

## What You Get

✅ Professional branded PDF statements  
✅ Company logo & header/footer  
✅ Clean, customer-friendly layout  
✅ Downloadable from partner page  
✅ Automatic date range filtering  
✅ Hidden confusing columns (Journal, Account #, Due Date, etc.)  

---

## Key Features

| Feature | Details |
|---------|---------|
| **Branding** | Company logo auto-displays in statement header |
| **Client-Friendly** | Hides internal accounting columns (Journal, Account #, etc.) |
| **Flexible Dating** | Supports any date range (defaults to current month) |
| **Professional Output** | Print-optimized PDF with company footer |
| **Custom Footer** | Add custom text per partner (payment terms, contact info, etc.) |

---

## Common Tasks

### Add Custom Footer to Statements

1. Open a partner record
2. Find **"Statement Footer"** field
3. Enter custom text:
   ```
   "Please pay within 30 days. Contact billing@company.com for questions."
   ```
4. Save ✅

### Change Date Range for Statement

When printing:
1. The report form appears
2. Modify the date range
3. Print ✅

Default: Current calendar month

### See Hidden Columns

The following columns are hidden in customer statements (visible only internally):
- ❌ Journal
- ❌ Account Number
- ❌ Due Date
- ❌ Matching/Reconciliation
- ❌ Amount Currency

**Visible columns:**
- ✅ Date
- ✅ Description/Activity
- ✅ Reference
- ✅ Amount
- ✅ Balance (running total)

---

## File Structure

```
partner_statement_branded/          ← The complete module
├── __manifest__.py                 ← Module info
├── models/
│   ├── account_partner_ledger.py   ← Column hiding logic
│   └── res_partner.py              ← Statement generation
├── report/
│   ├── customer_statements.py      ← Report handler
│   └── customer_statements_template.xml  ← PDF design
├── README.md                       ← Full documentation
├── INSTALLATION_GUIDE.md           ← Detailed setup
└── ...other support files
```

---

## Customization

### In 2 Minutes: Add Custom Company Banner

Edit: `report/customer_statements_template.xml`

Add after `<t t-call="web.external_layout">`:

```xml
<div style="padding: 20px; background: #007bff; color: white; text-align: center;">
    <h1>Thank You for Your Business!</h1>
</div>
```

---

## Troubleshooting

### Logo not showing?
✓ Upload logo in Settings → Company  
✓ Restart Odoo  
✓ Clear browser cache  

### Statement button missing?
✓ Refresh browser (Ctrl+R)  
✓ Check if module installed (Apps list)  
✓ Logout & login  

### Columns still visible?
✓ Clear cache  
✓ Restart Odoo server  
✓ Regenerate statement  

---

## Documentation

📖 **Full Documentation**: See [README.md](README.md)  
📖 **Installation Help**: See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)  
📖 **For Developers**: See [DEVELOPMENT.md](DEVELOPMENT.md)  
📖 **Version History**: See [CHANGELOG.md](CHANGELOG.md)  

---

## Next Steps

| What | Where |
|------|-------|
| **More documentation** | Read [README.md](README.md) |
| **Detailed setup** | Follow [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) |
| **Customize/extend** | Check [DEVELOPMENT.md](DEVELOPMENT.md) |
| **Report issues** | Document and contact admin |

---

## Support

**Questions?** Check the docs above.  
**Bugs?** See DEVELOPMENT.md troubleshooting section.  
**Need help?** Contact your Odoo administrator.

---

**Version:** 17.0.1.0.0  
**Status:** ✅ Production Ready  
**License:** AGPL-3.0  

**Happy Invoicing!** 📄✨
