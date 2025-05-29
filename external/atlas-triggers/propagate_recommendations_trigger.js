// MongoDB Atlas Trigger: Normalize and propagate recommendations
// Triggered on insert into `recommendations` collection

exports = async function(changeEvent) {
  const recDoc = changeEvent.fullDocument;
  if (!recDoc) {
    console.log(" No fullDocument — skipping");
    return;
  }

  // Extract fields from inserted recommendation document
  const userId = recDoc.userId;
  const invoiceId = recDoc.invoiceId;
  let itemsArray = Array.isArray(recDoc.items) ? recDoc.items : [];

  if (!userId || !invoiceId || itemsArray.length === 0) {
    console.log(" Missing required fields — skipping");
    return;
  }

  // Access MongoDB Atlas service and target database
  const mongodb = context.services.get("<YOUR-CLUSTER-NAME>");  // e.g., "Cluster0"
  const db = mongodb.db("<YOUR-DATABASE-NAME>");                // e.g., "my_app_db"

  // Ensure ObjectId format for user and invoice
  function ensureObjectId(id) {
    if (typeof id === "string") return BSON.ObjectId(id);
    return id;
  }

  // Normalize the structure:
  // Flatten `image` from object to string (URL)
  // Flatten `price` from object to raw number
  itemsArray = itemsArray.map(item => {
    if (typeof item.image === "object" && item.image.url) {
      item.image = item.image.url;
    }

    if (typeof item.price === "object" && item.price.amount) {
      item.price = item.price.amount;
    }

    return item;
  });

  try {
    // Save the latest recommendations in the user document
    await db.collection("users").updateOne(
      { _id: ensureObjectId(userId) },
      { $set: { lastRecommendations: itemsArray } },
      { upsert: true }
    );

    // Limit the items array to the first 6 elements and store it in the invoice document
    const limitedItemsArray = itemsArray.slice(0, 6); // Keeps only the first 6 items
    
    await db.collection("invoices").updateOne(
      { _id: ensureObjectId(invoiceId) },
      { $set: { recommendations: limitedItemsArray } }
    );

    console.log(`✅ Trigger updated user and invoice documents successfully`);
  } catch (err) {
    console.error("❌ Trigger failed:", err.message);
  }
};
