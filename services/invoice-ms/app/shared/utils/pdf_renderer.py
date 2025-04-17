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
            <h1>Invoice #{invoice_id}</h1>
            <p><strong>Date:</strong> {created_at}</p>

            <h2>Items</h2>
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Price</th>
                  <th>Quantity</th>
                </tr>
              </thead>
              <tbody>
        """

        # Add each item as a table row
        for item in items:
            name = item.get("name", "Product")
            price = item.get("price", {}).get("amount", 0)
            amount = item.get("amount", 1)
            html += f"<tr><td>{name}</td><td>${price:.2f}</td><td>{amount}</td></tr>"

        # Add total and ERP metadata
        html += f"""
              </tbody>
            </table>

            <p class="total">Total: ${total:.2f}</p>

            <h3>ERP Details</h3>
            <p><strong>ERP Invoice Number:</strong> {metadata.get('invoiceNumber', '---')}</p>
            <p><strong>Due Date:</strong> {metadata.get('dueDate', '---')}</p>
            <p><strong>Payment Terms:</strong> {metadata.get('paymentTerms', '---')}</p>
        """

        # Add recommended products only if present
        if recommendations:
            html += """
              <div class="recommendations">
                <h2>Recommended Products</h2>
            """
            for rec in recommendations:
                product_id = rec.get("productId", "")
                name = rec.get("name", "")
                image_url = rec.get("image", "https://via.placeholder.com/150")
                product_link = f"https://store.com/product/{product_id}"

                html += f"""
                  <div class="product">
                    <a href="{product_link}">
                      <img src="{image_url}" alt="{name}" />
                    </a>
                    <div class="product-name">{name}</div>
                  </div>
                """
            html += "</div>"

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
