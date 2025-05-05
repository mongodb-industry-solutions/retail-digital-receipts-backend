# Mock Invoice Enrichment Function

This repository provides a mock implementation of an Azure Function that simulates invoice enrichment metadata.  
It is designed for **demos, local testing** that need enrichment logic before generating invoices.

---

## What does it do?

This Azure Function receives an **HTTP POST** request with order data and returns simulated metadata similar to what you would get from:

- ERP systems (invoicing details)
- Fraud detection engines (risk score)
- Loyalty programs (reward points)
- Credit card processors (approval info)
- POS systems (terminal info)

---

## Example input (POST body)

```json
{
  "_id": "67ff87acaf5e3450b5d69c06",
  "products": [
    {
      "amount": 1,
      "brand": "Mama Bear",
      "code": "MB3AR_6",
      "description": "",
      "_id": "67192b3f64d161905fbe779a",
      "image": {
        "url": "https://m.media-amazon.com/images/I/71zbEs2EP+L.jpg"
      },
      "name": "Mama Bear Soft Lightly Fragranced Wipes, Pack of 4, 224-Count",
      "price": {
        "amount": 26,
        "currency": null
      }
    }
  ],
  "shipping_address": "Av. Lázaro Cárdenas 305, Guadalajara 44030, Mexico",
  "status_history": [
    {
      "status": "In process",
      "timestamp": 1744799660381.0
    }
  ],
  "type": "Buy Online, Pick up in Store",
  "user": "671ff0081ec726b417352702"
}
```

---

## Example output (response)

```json
{
  "erpDetails": {
    "invoiceNumber": "ERP-67ff87acaf5e3450b5d69c06",
    "paymentTerms": "Net 30",
    "dueDate": "2025-04-16",
    "subtotal": 26,
    "totalTax": 6.76,
    "discount": 10.0,
    "totalAmount": 22.76
  },
  "fraudDetection": {
    "riskScore": 3,
    "status": "passed"
  },
  "loyaltyRewards": {
    "pointsEarned": 50,
    "tier": "Gold"
  },
  "creditCardProcessing": {
    "approvalCode": "APPROVED123",
    "transactionId": "TX-67ff87acaf5e3450b5d69c06-103420"
  },
  "posData": {
    "terminalId": "POS-001",
    "location": "Store #1, Sample City",
    "transactionTime": "2025-04-16T10:34:20.598212"
  },
  "retrievedAt": "2025-04-16T10:34:20.598216"
}
```

---

## Why Azure Functions?

We chose **Azure Functions** for this demo because they offer an ideal way to simulate external services in a clean, cost-efficient, and serverless manner.

### Benefits:

- **Pay-as-you-go model**: You’re only charged for the actual execution time. No need to maintain idle infrastructure.
- **Serverless and scalable**: Automatically scales with the load — no manual intervention required.
- **Easy to deploy**: You can build and publish functions from the Azure Portal, CLI, or even GitHub.
- **Perfect for mocks or external integrations**: In real-world systems, external metadata (like ERP or fraud scores) often comes from remote services. This function mimics that pattern without needing a full backend or API gateway.

> Ideal for testing event-driven architectures like microservices, serverless invoicing, and mock APIs.

---

## 🔧 Deployment

This function is built for [Azure Functions (Python)](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python).  

> Requires Python 3.10+

---
## License

© 2025 MongoDB. All rights reserved.

This repository is intended solely for demonstration and educational purposes.  
Commercial use is strictly prohibited without written permission from MongoDB.  
No support or warranty is provided. Use at your own risk.