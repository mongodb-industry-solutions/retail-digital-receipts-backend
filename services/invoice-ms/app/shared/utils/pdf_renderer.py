from weasyprint import HTML
import os
from datetime import datetime

class InvoiceRenderer:
    def render(self, invoice: dict) -> str:
        # Extract invoice ID (handle ObjectId format from MongoDB)
        invoice_id = invoice["_id"]["$oid"] if isinstance(invoice["_id"], dict) else invoice["_id"]

        # Use the createdAt date or fallback to today's date
        created_at = invoice.get("createdAt", datetime.utcnow().isoformat())[:10]

        # Extract line items from the invoice
        items = invoice.get("items", [])

        # Extract ERP-related metadata
        metadata = invoice.get("metadata", {}).get("erpDetails", {})

        # Limit to 4 product recommendations (optional)
        recommendations = invoice.get("recommendations", [])[:4]

        # Get total amount (from metadata or fallback)
        subtotal = metadata.get("subtotal", invoice.get("subtotal", 0))
        tax = metadata.get("totalTax", invoice.get("totalTax", 0))
        total = metadata.get("totalAmount", invoice.get("totalAmount", 0))

        # Begin HTML content
        html = f"""
        <html>
          <head>
            <style>
              body {{
                font-family: sans-serif;
                padding: 40px;
                color: #333;
              }}
              h1 {{ color: #4CAF50; }}
              table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
              }}
              th, td {{
                border: 1px solid #ddd;
                padding: 8px;
              }}
              th {{ background-color: #f2f2f2; }}
              .total {{
                text-align: right;
                font-size: 18px;
                font-weight: bold;
              }}
              .recommendations {{
                margin-top: 40px;
              }}
              .product {{
                display: inline-block;
                width: 22%;
                text-align: center;
                margin: 1%;
              }}
              .product img {{
                width: 100%;
                max-width: 150px;
                border-radius: 6px;
              }}
              .product-name {{
                font-size: 12px;
                margin-top: 6px;
              }}
            </style>
          </head>
          <body>
            <h1>Pop-Up Store</h1>
            <small>Created in {created_at}</small>
            <small>Order Id {invoice_id}</small>
            <h2>Items</h2>
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Product</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
        """

        # Add each item as a table row
        i = 1
        for item in items:
            name = item.get("name", "Product")
            price = item.get("price", {}).get("amount", 0)
            amount = item.get("amount", 1)
            html += f"<tr><td>{1}</td><td>{name}</td><td>{amount} x ${price:.2f}</td></tr>"
            i = i+1

        # Add total and ERP metadata
        html += f"""
              </tbody>
            </table>

            <p class="total">Subtotal: ${subtotal:.2f}</p>
            <p class="total">Tax: ${tax:.2f}</p>
            <p class="total">Total: ${total:.2f}</p>            
        """

        # Add recommended products only if present
        html +=  f"""<div class='products-container'>
              <p class="ms-0">Based on this order you might also like</p>
              <div class='recommendations-list mt-3'>"""
        for rec in recommendations:
            name = rec.get("name", "")
            brand = rec.get("brand", "")
            image_url = rec.get("image", "https://via.placeholder.com/150")
            vectorSearchScore = rec.get("vectorSearchScore", "")

            html += f"""
              <div class="product">
                <img src="{image_url}" alt="{name}" />
                <div class="product-name">{name}</div>
              </div>

                      <div class='PRCard cursorPointer' >
            <div class='d-flex flex-column'>
                <div class='scoreContainer'>
]                        <div class='scorebadge' variant="yellow">
                            {vectorSearchScore}
                        </div>
                </div>
                <div class='imageContainer'>
                     <img
                            src={image_url}
                            alt={name}
                            fill
                            quality={50}
                            unoptimized
                            style={{ objectFit: "contain" }}
                        />
                </div>
                <div class='ms-3 me-3 mt-3'>
                    <p class="name" title={name}>{name}</p>
                    <p class="brand" title={brand}>{brand}</p>
                </div>
            </div>
        </div>
            """
        html += """ </div>
          </div>"""

        # Final HTML closing
        html += """
          </body>
        </html>
        """

        # Generate PDF file in /tmp directory
        file_path = f"/tmp/invoice_{invoice_id}.pdf"
        HTML(string=html).write_pdf(file_path)

        # Return the file path for further processing (e.g., upload to blob)
        return file_path
