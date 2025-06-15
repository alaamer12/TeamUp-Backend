const mongoose = require('mongoose');

// Get MongoDB connection string from environment variables
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/teamup';

// Connect to MongoDB
async function connectToDatabase() {
  try {
    // Add connection options specifically for Vercel serverless environment
    await mongoose.connect(MONGODB_URI, {
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
      family: 4 // Force IPv4
    });
    console.log('Connected to MongoDB');
    return mongoose.connection;
  } catch (error) {
    console.error('Failed to connect to MongoDB:', error);
    // Don't exit process in production/serverless environment
    if (process.env.NODE_ENV !== 'production') {
      process.exit(1);
    }
    throw error; // Re-throw the error for handling in serverless context
  }
}

// Add a cached connection for serverless environment
let cachedConnection = null;

async function getDatabaseConnection() {
  // For serverless environment (Vercel), reuse connection if available
  if (cachedConnection) {
    return cachedConnection;
  }
  
  cachedConnection = await connectToDatabase();
  return cachedConnection;
}

module.exports = { connectToDatabase, getDatabaseConnection }; 