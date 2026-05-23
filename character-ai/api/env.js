module.exports = function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.status(200).json({
    API_KEY: process.env.API_KEY || '',
    PROVIDER: process.env.PROVIDER || 'groq',
    MODEL: process.env.MODEL || 'llama-3.3-70b-versatile',
    THEME: process.env.THEME || 'dark'
  });
};
