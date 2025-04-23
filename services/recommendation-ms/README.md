# 🧠 recommendation-ms

Generates personalized product suggestions based on new purchases.  
Built with MongoDB Atlas Vector Search, asynchronous queues, and a clean architecture approach.

---

## 🔍 What it does

Every time an invoice is created, `recommendation-ms`:

1. Extracts the most expensive product from the invoice.
2. Retrieves its vector embedding (pre-computed with Voyage AI, stored in the `products` collection).
3. Performs a vector similarity search against the `products` catalog using MongoDB Atlas Vector Search.
4. Selects the top 4 similar products and wraps them into a `RecommendationGroup`.
5. Stores the result in the `recommendations` collection.
6. Lets an Atlas Trigger propagate the data to:
   - `users.lastRecommendations`
   - `invoices.recommendations`
7. The frontend displays results directly from user and invoice documents — no extra API calls.

---

## 🧭 Architecture Diagram

![Architecture](docs/images/recommendation-ms.png)

---

## 🧱 Architecture Design

- **Event-Driven Choreography**  
  Each service reacts to MongoDB inserts; no service calls another directly.

- **Event-Carried State Transfer (ECST)**  
  The entire recommendation payload is stored in `recommendations`. The Trigger simply copies that document to other collections.

- **Separation of Concerns**  
  `recommendation-ms` only writes to its own collection. Updates to `users` and `invoices` are handled externally by the Atlas Trigger.

---

## 📦 Setup Instructions

1. Copy `.env.example` to `.env` and update the values with your environment.

2. Make sure your MongoDB cluster includes:
   - ✅ Embeddings stored in the `products.embedding` field  
   - ✅ A vector index on that field (`product_vector_index`)  
   - ✅ An Atlas Trigger configured for `recommendations.insert`

3. You can run this service in two ways:
   - Using **Poetry** locally for development.
```bash

poetry install
poetry shell
uvicorn main:app --reload
```

   - Or using **Docker** with the provided `Dockerfile`.
```bash

docker build -t recommendation-ms .
docker run --env-file .env -p 8000:8000 recommendation-ms
```
---

## 🧪 Status

- ✅ Functional prototype  
- 🛠️ Ready for load testing & analytics pipeline integration  
- 📈 Ideal entry point for experimentation with Vector Search + Atlas Triggers
