# 🧾 Retail Digital Receipt Demo / Event-Driven Microservices with MongoDB & Azure

This project showcases how to build a **document-centric, event-driven e-commerce architecture** using **MongoDB Atlas** and **Azure microservices**.

The solution simulates the generation of digital receipts and personalized recommendations.

---

## 🎯 Demo Goals

- Show how **Change Streams** and **Triggers** can power microservices in an event-driven architecture (EDA) 
- Highlight the power of **MongoDB Atlas** for flexible, document-based modeling and fast data retrieval
- Simulate **external system integrations** - such as taxes, fraud detection and loyalty points - quickly and easily via **Azure Functions**  
- Deliver real-time **personalized recommendations** using **MongoDB Vector Search** and **VoyageAI**
- Keep the architecture clean, reactive, and production-inspired, but demo-friendly  

> 💡 The frontend and core backend services (orders, users) are hosted on **Google Cloud Platform (GCP)**, while the microservices for invoices and recommendations are implemented in **Azure**.
---

## 🧩 Architecture Overview

> 📌 _Image: Adding Digital Receipts in Leafy Store_  
![image](./docs/images/adding-digital-receipts-leafy-store.png)



| Component        | Cloud | Role |
|------------------|-------|------|
| **Frontend & Order/User Management** | GCP (Next.js) | User interface and order processing |
| **Invoice & Recommendation Services** | Azure App Service | Event-driven invoice creation and instant recommendation for the user  |
| **MongoDB Atlas** | MongoDB Atlas | Centralized data layer for orders, invoices, users, and recommendations |
| **Azure Function** | Azure | Mocks external system metadata for invoices |
| **Voyage AI**     | External | Provides product vector embeddings |

> 📝 _Note 1: While this demo uses a single shared MongoDB Atlas database, in production, each service would typically use its own database, enabling greater isolation, scalability, and data governance._

> 📝 _Note 2: In this demo, services are distributed across different cloud providers (e.g., Azure for backend microservices and GCP for the frontend). This setup reflects our team's decision to experiment with cross-cloud scenarios. However, from an architectural perspective, all components can be deployed locally or within a single cloud provider, depending on your environment and preferences._

---

## 🔄 System Flow Highlights

> 📌 _Image: Purchase Workflow_  
![image](./docs/images/digital-receipts-activity-diagram.png)

---

## 👤 Use Cases In This Demo:

### 1 - ⚡ Event-Driven Invoice Creation  
> Automatically generate invoices in response to new orders using MongoDB Change Streams  
📌 _Architecture Use Case 1_  
![Architecture Use Case 1](./docs/images/create-invoice-architecture-ecosystem.png)

### 2 - 🧾 Download Invoice  
> Retrieve and display invoice files stored in Blob Storage or generated on demand.  
📌 _Architecture Use Case 2_  
![Architecture Use Case 2](./docs/images/get-invoice-architecture-ecosystem.png)

### 3 - 🔮 Instant Recommendation for the User  
> Deliver personalized product suggestions based on recent purchases, using Vector Search.  
📌 _Set-Up Use Case 3_  
![Set-Up Use Case 3](./docs/images/personalization-set-up.png)  
📌 _Architecture Use Case 3_  
![Architecture Use Case 3](./docs/images/instant-recommendation-to-the-user.png)

---

## 🏗️ From High-Level Design to Implementation Details

This demo balances **macro-level architecture** with **implementation details** to showcase a fully event-driven flow powered by **MongoDB Change Streams**.

> For simplicity, we use an **in-memory queue in Python** — easily replaceable with production-ready tools like **Azure Service Bus**, **Event Grid**, **Storage Queues**, or **Kafka** via the [MongoDB Kafka Connector](https://www.mongodb.com/docs/kafka-connector/current/).

> 📌 _Image: Event-Driven Invoice Processing Internals_  
![image](./docs/images/eda-easy-integarton.png)

> 📝 _Note 3: This architecture is designed for extensibility — swap the in-memory queue with any event broker without changing the core flow._

---

## 🗂️ Folder Structure

```bash
/services
  ├── invoice-ms/                         
  └── recommendation-ms/                 

/external
  └── azure_function_invoice_mock.py       

docs/
  └── adr/

docker-compose.yml
.env.example
Makefile
```
> 📝 _Note : Curious about how and why this system was designed? Read the ADR documentation (Architecture Decision Records) to explore the reasoning behind key architectural and modeling decisions._
---

## 📎 Go to Related Components for Setup Instructions and Microservice Details

- 📄 [`services/invoice-ms/README.md`](services/invoice-ms/README.md)  
- 📄 [`services/recommendation-ms/README.md`](services/recommendation-ms/README.md)  
- 📄 [`external/README.md`](external/README.md)  

🔗 To configure the frontend and backend for `order` and `user`, please refer to our previous demo — the starting point for this project: [retail-store-v2](https://github.com/mongodb-industry-solutions/retail-store-v2)

---

## 💡 By storing your **invoice data in MongoDB**, you unlock a host of benefits:

- 🔐 **Security & Data Privacy**  
  MongoDB Atlas offers field-level encryption, role-based access control (RBAC), auditing, and network isolation, making it ideal for handling sensitive billing and customer data.

- 🌍 **Geographical Compliance & Sharding**  
  Global clusters and zone sharding help you comply with regulations like GDPR and CCPA while keeping data close to the user for low-latency access.

- 📊 **Workload Isolation for Analytics**  
  MongoDB enables real-time analytics on invoice data—using read-only secondaries or Atlas Data Federation—without disrupting core transaction workloads.

- 🔄 **From Data Silos to Seamless Access**  
  Invoice data often lives isolated in backend systems like ERPs or legacy databases, making real-time access difficult and creating silos that block innovation and personalization. By storing invoices as rich, flexible documents in MongoDB, you unlock seamless cross-service access and turn billing data into a driver for real-time insights and intelligent experiences.

---

## 👥 Authors & Contributors

This project was made possible through a close collaboration between domain experts and technical implementers:

### Lead Authors *(Use Case Ideation & Retail Implementation)*
- [**Rodrigo Leal**](https://www.linkedin.com/in/rodrigo-leal-5b240121/) – Principal
- [**Prashant Juttukonda**](https://www.linkedin.com/in/cloudpkj/) – Principal  
- [**Genevieve Broadhead**](https://www.linkedin.com/in/genevieve-broadhead-271757bb/) – Global Lead, Retail Solutions  

### Developers & Maintainers *(Technical Design & Implementation)*
- [**Florencia Arin**](https://www.linkedin.com/in/floarin/) – Developer & Maintainer
- [**Angie Guemes**](https://www.linkedin.com/in/angelica-guemes-estrada/) – Developer & Maintainer  


---

## 📚 Related Blogs *(Coming Soon)*

- **Blog 1** – *Coming soon...*
- **Blog 2** – *Coming soon...*




