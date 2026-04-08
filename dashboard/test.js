const API_KEY = 'AIzaSyBuTVVcshyMaaJPTGh_GXMVZMbE83gyQoM';
const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ contents: [{ parts: [{ text: 'hello' }] }] })
}).then(res => {
  console.log(res.status);
  return res.text();
}).then(console.log).catch(console.error);
