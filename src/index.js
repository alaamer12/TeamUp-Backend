const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const { getDatabaseConnection } = require('./config/database');
const TeamRequest = require('./models/TeamRequest');
require('dotenv').config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 8080;

// Connect to MongoDB - For serverless, we'll connect at request time
// We'll initialize connection once for local development
if (process.env.NODE_ENV !== 'production') {
  getDatabaseConnection().catch(console.error);
}

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());
app.use(morgan('dev'));

// Connection middleware for serverless environments
const ensureDbConnected = async (req, res, next) => {
  if (process.env.NODE_ENV === 'production') {
    try {
      await getDatabaseConnection();
      next();
    } catch (error) {
      console.error('Database connection failed:', error);
      res.status(500).json({ error: 'Database connection failed' });
    }
  } else {
    next();
  }
};

// Apply DB connection middleware to routes that need DB access
app.use('/api', ensureDbConnected);

// API Routes
app.get('/api/requests', async (req, res) => {
  try {
    const requests = await TeamRequest.find().sort({ createdAt: -1 });
    res.json(requests);
  } catch (error) {
    console.error('Error fetching requests:', error);
    res.status(500).json({ error: 'Failed to fetch requests' });
  }
});

app.post('/api/requests', async (req, res) => {
  try {
    const newRequest = new TeamRequest(req.body);
    const savedRequest = await newRequest.save();
    res.status(201).json(savedRequest);
  } catch (error) {
    console.error('Error creating request:', error);
    res.status(500).json({ error: 'Failed to create request' });
  }
});

app.delete('/api/requests/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { ownerFingerprint } = req.body;
    
    // Find the request
    const request = await TeamRequest.findById(id);
    
    if (!request) {
      return res.status(404).json({ error: 'Request not found' });
    }
    
    // Check ownership
    if (request.ownerFingerprint !== ownerFingerprint) {
      return res.status(403).json({ error: 'Not authorized to delete this request' });
    }
    
    // Delete the request
    await TeamRequest.findByIdAndDelete(id);
    
    res.json({ message: 'Request deleted successfully' });
  } catch (error) {
    console.error('Error deleting request:', error);
    res.status(500).json({ error: 'Failed to delete request' });
  }
});

app.put('/api/requests/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updatedData = req.body;
    
    // Find the request
    const request = await TeamRequest.findById(id);
    
    if (!request) {
      return res.status(404).json({ error: 'Request not found' });
    }
    
    // Check ownership
    if (request.ownerFingerprint !== updatedData.ownerFingerprint) {
      return res.status(403).json({ error: 'Not authorized to update this request' });
    }
    
    // Update the request
    const updatedRequest = await TeamRequest.findByIdAndUpdate(
      id,
      { ...updatedData, updatedAt: new Date() },
      { new: true }
    );
    
    res.json(updatedRequest);
  } catch (error) {
    console.error('Error updating request:', error);
    res.status(500).json({ error: 'Failed to update request' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date(),
    environment: process.env.NODE_ENV,
    version: '1.0.2'
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({ 
    message: 'TeamUp API is running',
    docs: '/api-docs',
    health: '/health'
  });
});

// Handle 404
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// For local development
if (process.env.NODE_ENV !== 'production') {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

// For Vercel
module.exports = app; 