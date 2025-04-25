exports = async function(changeEvent) {
  // The full document inserted into the `recommendations` collection
  const recDoc = changeEvent.fullDocument;
  if (!recDoc) {
    console.log("No fullDocument — skipping trigger");
    return;
  }

  // Extract the user ID and ensure we have an array of recommendation items
  const userId = recDoc.userId;
  const itemsArray = Array.isArray(recDoc.items)
    ? recDoc.items
    : (recDoc.items ? [recDoc.items] : []);

  // Get a handle to the Atlas service and the target database
  const mongodb = context.services.get("IST-Shared");
  const db = mongodb.db("leafy_popup_store");

  // 1) Update the user's document: set `lastRecommendations` to the array of items
  await db.collection("users").updateOne(
    { _id: userId },                            // Match by user ObjectId
    { $set: { lastRecommendations: itemsArray } }, // Overwrite with latest recommendations
    { upsert: true }                             // Create user doc if it doesn't exist
  );

  // 2) Update the corresponding invoice: store the same items array under `recommendations`
  await db.collection("invoices").updateOne(
    { _id: BSON.ObjectId(recDoc.invoiceId) },   // Convert invoiceId string back to ObjectId
    { $set: { recommendations: itemsArray } }     // Save recommendation items on the invoice
  );
};
