from docxtpl import DocxTemplate

doc = DocxTemplate("/home/user/temp2/sample_template.docx")

context = {
    "company_name": "Acme Corp",
    "company_address": "123 Main Street, Hyderabad",
    "company_email": "sales@acme.com",
    "company_phone": "+91 98765 43210",
    "quote_date": "June 5, 2026",
    "quote_id": "Q-2026-001",
    "client_name": "Charith Kumar",
    "client_company": "Charith Tech",
    "client_address": "456 Park Avenue, Bangalore",
    "product_name": "Pro Plan",
    "project_description": "annual software subscription",
    "subtotal": "$1,000",
    "tax": "$180",
    "grand_total": "$1,180",
    "valid_until": "June 30, 2026",
    "sender_name": "Jane Doe",
    "sender_title": "Sales Manager",
    "items": [
        {"name": "Setup fee", "qty": 1, "rate": "$500", "total": "$500"},
        {"name": "Monthly subscription", "qty": 2, "rate": "$250", "total": "$500"},
    ],
}

doc.render(context)
doc.save("/home/user/temp2/sample_filled.docx")
print("saved sample_filled.docx")
