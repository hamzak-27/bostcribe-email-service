// Local development server for Vercel functions
const { exec } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

console.log('Starting development server for Vercel functions...');
console.log('Press Ctrl+C to stop');

// Start the server
const server = http.createServer((req, res) => {
  console.log(`Request received: ${req.method} ${req.url}`);
  
  // Map the URL to the corresponding API endpoint based on vercel.json routes
  const routes = {
    '/send-contact-email': '/api/send-contact-email.py',
    '/send-schedule-email': '/api/send-schedule-email.py',
    '/health': '/api/health.py'
  };
  
  const endpoint = routes[req.url];
  if (!endpoint) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  
  // Execute the Python script
  const pythonScript = path.join(__dirname, endpoint);
  exec(`python ${pythonScript}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      res.writeHead(500);
      res.end('Internal Server Error');
      return;
    }
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(stdout);
  });
});

server.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
}); 