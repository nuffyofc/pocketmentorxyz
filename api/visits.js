// Real site-visit counter backed by Vercel KV (Upstash Redis REST API).
// Requires a KV/Redis database attached to this Vercel project (Storage tab
// -> Create Database -> KV). Vercel may inject the env vars either as
// KV_REST_API_URL/KV_REST_API_TOKEN or prefixed with the store's name
// (e.g. storage_KV_REST_API_URL), so we check both.
module.exports = async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');

  const url = process.env.KV_REST_API_URL || process.env.storage_KV_REST_API_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.storage_KV_REST_API_TOKEN;

  if (!url || !token) {
    res.status(200).json({ value: null, error: 'KV not configured' });
    return;
  }

  try {
    const r = await fetch(`${url}/incr/site_visits`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await r.json();
    res.status(200).json({ value: data.result });
  } catch (err) {
    res.status(200).json({ value: null, error: 'KV request failed' });
  }
};
