"""
Mock Invoice Enrichment Function
--------------------------------

Author: Florencia Arin
Created for: Retail Invoice Microservice Demo

Mock Invoice Enrichment Service (Azure Function)

This function simulates the response from external services typically involved
in invoice generation workflows—such as ERP systems, fraud detection, loyalty programs,
POS systems, and payment processing platforms.

It receives order data via HTTP POST and returns enriched metadata as JSON.

Usage:
This mock is intended for educational purposes, testing, and prototyping.

"""
import azure.functions as func
import logging
import json
from datetime import datetime

# Azure Function App with anonymous access
# Intended for use in demos, local testing, or prototyping microservices
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="mock-enrichment")  # Public-safe and generic route name
def enrichment_mock(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Invoice enrichment request received.")

    # Try to parse the incoming request body as JSON
    try:
        order_data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON in request.", status_code=400)

    # Extract order ID and product list
    order_id = str(order_data.get("_id", "unknown"))
    products = order_data.get("products", [])

    # Simulate basic financial summary
    subtotal = sum(item.get("price", {}).get("amount", 0) for item in products)
    vat_rate = 0.21
    service_tax_rate = 0.05
    total_tax = subtotal * (vat_rate + service_tax_rate)
    discount = 10.0  # Fixed discount (example)
    total_amount = subtotal + total_tax - discount

    # Construct the enrichment metadata payload
    enrichment = {
        "erpDetails": {
            "invoiceNumber": f"ERP-{order_id}",
            "paymentTerms": "Net 30",
            "dueDate": datetime.utcnow().strftime("%Y-%m-%d"),
            "subtotal": subtotal,
            "totalTax": total_tax,
            "discount": discount,
            "totalAmount": total_amount
        },
        "fraudDetection": {
            "riskScore": 3,  # Example score on a 0–10 scale
            "status": "passed"
        },
        "loyaltyRewards": {
            "pointsEarned": 50,
            "tier": "Gold"
        },
        "creditCardProcessing": {
            "approvalCode": "APPROVED123",
            "transactionId": f"TX-{order_id}-{datetime.utcnow().strftime('%H%M%S')}"
        },
        "posData": {
            "terminalId": "POS-001",
            "location": "Store #1, Sample City",  # Public-safe placeholder
            "transactionTime": datetime.utcnow().isoformat()
        },
        "retrievedAt": datetime.utcnow().isoformat()
    }

    logging.info(f"Enrichment metadata generated for order {order_id}")

    return func.HttpResponse(
        json.dumps(enrichment),
        mimetype="application/json",
        status_code=200
    )
