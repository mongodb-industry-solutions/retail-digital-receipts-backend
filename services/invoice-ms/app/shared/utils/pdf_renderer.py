from weasyprint import HTML
import os
from datetime import datetime

class InvoiceRenderer:
    def render(self, invoice: dict) -> str:
        # Extract invoice ID (handle ObjectId format from MongoDB)
        invoice_id = invoice["_id"]["$oid"] if isinstance(invoice["_id"], dict) else invoice["_id"]

        # Use the createdAt date or fallback to today's date
        created_at = invoice.get("createdAt", datetime.utcnow().isoformat())[:10]

        # Extract line items and ERP-related metadata
        items = invoice.get("items", [])
        metadata = invoice.get("metadata", {}).get("erpDetails", {})

        # Limit to 4 recommendations
        recommendations = invoice.get("recommendations", [])[:4]

        # Get totals
        subtotal = metadata.get("subtotal", invoice.get("subtotal", 0))
        tax = metadata.get("totalTax", invoice.get("totalTax", 0))
        total = metadata.get("totalAmount", invoice.get("totalAmount", 0))

        # Get base store URL from environment variables
        store_url = os.getenv("STORE_URL", "http://localhost:3000/shop")

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
                text-align: left;
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
              .products-container {{
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
              }}
              .product {{
                text-align: center;
                width: 22%;
              }}
              .product img {{
                width: 100%;
                max-width: 120px;
                height: 120px;
                object-fit: contain;
                border-radius: 6px;
                margin-bottom: 6px;
              }}
              .product-name {{
                font-size: 12px;
                margin-bottom: 2px;
              }}
              .product-price {{
                font-size: 12px;
                font-weight: bold;
                color: #555;
              }}
              a {{
                text-decoration: none;
                color: inherit;
              }}
            </style>
          </head>
          <body>
            <h1>Pop-Up Store</h1>
            <small>Created on {created_at}</small><br/>
            <small>Order ID: {invoice_id}</small>

            <h2>Items</h2>
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
        """

        # Add each item as a table row with image and name
        for item in items:
            name = item.get("name", "Product")
            amount = item.get("amount", 1)

            # Extract price safely
            price = item.get("price", 0)
            if isinstance(price, dict):
                price = price.get("amount", 0)

            # Extract image URL safely
            image_url = item.get("image", "https://via.placeholder.com/50")
            if isinstance(image_url, dict):
                image_url = image_url.get("url", "https://via.placeholder.com/50")

            html += f"""
            <tr>
              <td>
                <img src="{image_url}" alt="{name}" style="width: 50px; height: 50px; object-fit: contain; vertical-align: middle; margin-right: 10px;">
                {name}
              </td>
              <td>{amount} x ${price:.2f}</td>
            </tr>
            """

        # Add total and ERP metadata
        html += f"""
              </tbody>
            </table>

            <p class="total">Subtotal: ${subtotal:.2f}</p>
            <p class="total">Tax: ${tax:.2f}</p>
            <p class="total">Total: ${total:.2f}</p>
        """

        # Add recommendations if available
        if recommendations:
            html += """
            <div class="recommendations">
              <h2>Based on this order you might also like</h2>
              <div class="products-container">
            """

            for rec in recommendations:
                name = rec.get("name", "Unnamed Product")

                # Extract price safely
                price = rec.get("price", 0)
                if isinstance(price, dict):
                    price = price.get("amount", "N/A")

                # Extract image safely
                image_url = rec.get("image", "https://via.placeholder.com/150")
                if isinstance(image_url, dict):
                    image_url = image_url.get("url", "https://via.placeholder.com/150")

                html += f"""
                <div class="product">
                  <a href="{store_url}" target="_blank">
                    <img src="{image_url}" alt="{name}" />
                    <div class="product-name">{name}</div>
                    <div class="product-price">${price}</div>
                  </a>
                </div>
                """

            html += """
              </div>
            </div>
            """

        # Final HTML closing
        html += """
          </body>
        </html>
        """

        # Generate PDF
        file_path = f"/tmp/invoice_{invoice_id}.pdf"
        HTML(string=html).write_pdf(file_path)

        return file_path
