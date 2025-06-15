const mongoose = require('mongoose');

const memberSchema = new mongoose.Schema({
  tech_field: [String],
  gender: String,
  major: String,
  planguage: [String],
  already_know: Boolean
}, { _id: false });

const teamRequestSchema = new mongoose.Schema({
  id: {
    type: String,
    trim: true
  },
  user_personal_phone: {
    type: String,
    trim: true
  },
  user_name: {
    type: String,
    trim: true,
    required: true
  },
  user_gender: {
    type: String,
    trim: true
  },
  user_abstract: {
    type: String,
    trim: true
  },
  members: [memberSchema],
  ownerFingerprint: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

// Update the updatedAt field before saving
teamRequestSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

const TeamRequest = mongoose.model('TeamRequest', teamRequestSchema);

module.exports = TeamRequest; 