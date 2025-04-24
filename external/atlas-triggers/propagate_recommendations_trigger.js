exports = async function(changeEvent) {
    const fullDoc = changeEvent.fullDocument;
    const { userId, invoiceId, recommendations } = fullDoc;
  
    const db = context.services.get("<your-linked-cluster>").db("<your-database-name>");
  
    // Update user document
    await db.collection("users").updateOne(
      { _id: userId },
      { $set: { lastRecommendations: recommendations } }
    );
  
    // Update invoice record
    await db.collection("invoices").updateOne(
      { _id: invoiceId },
      { $set: { recommendations: recommendations } }
    );
  };
  