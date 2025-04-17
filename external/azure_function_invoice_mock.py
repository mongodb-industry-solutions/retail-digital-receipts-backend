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
    """
    Simulates an external enrichment service for invoices.

    This Azure Function receives order data via HTTP POST,
    and returns mock enrichment metadata typically provided by external systems
    such as ERP, payment processors, loyalty engines, and fraud detection tools.
    
    It's used by a backend invoice microservice to mimic real-world metadata enrichment.
    """
    logging.info("Received request for detailed invoice enrichment.")

    # Attempt to parse the JSON payload from the request
    try:
        order_data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON in request.", status_code=400)

    # Extract order ID and product list from the request body
    order_id = str(order_data.get("_id", "unknown"))
    products = order_data.get("products", [])

    try:
        # Simulate a financial summary based on the products in the order
        total_amount = sum(item.get("price", {}).get("amount", 0) for item in products)
        vat_rate = 0.21
        service_tax_rate = 0.05
        total_tax = total_amount * (vat_rate + service_tax_rate)
        subtotal = total_amount - total_tax
    except Exception as e:
        logging.error(f"Error during enrichment: {e}")
        return func.HttpResponse("Error processing request", status_code=500)
        
    # Build the enrichment metadata dictionary
    enrichment = {
        "erpDetails": {
            "invoiceNumber": f"ERP-{order_id}",
            "paymentTerms": "Net 30",
            "dueDate": datetime.utcnow().strftime("%Y-%m-%d"),
            "subtotal": subtotal,
            "totalTax": total_tax,
            "totalAmount": total_amount
        },
        "fraudDetection": {
            "riskScore": 3,  # Arbitrary low risk
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
        "retrievedAt": datetime.utcnow().isoformat()
    }

    # Log the generated metadata for observability
    logging.info(f"Generated enrichment metadata for order {order_id}: {enrichment}")

    # Return the simulated metadata as JSON
    return func.HttpResponse(
        json.dumps(enrichment),
        mimetype="application/json",
        status_code=200
    )
