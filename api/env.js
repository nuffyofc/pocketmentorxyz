export default function handler(req) {
  const env = {
    API_KEY: process.env.API_KEY || '',
    PROVIDER: process.env.PROVIDER || 'groq',
    MODEL: process.env.MODEL || 'llama-3.3-70b-versatile',
    THEME: process.env.THEME || 'dark'
  };
  return new Response(JSON.stringify(env), {
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  });
}
