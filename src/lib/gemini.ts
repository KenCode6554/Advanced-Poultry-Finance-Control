const API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

if (!API_KEY) {
  console.error("Missing VITE_GOOGLE_API_KEY");
}


export const getGeminiResponse = async (prompt: string, files?: { url: string, mimeType: string }[]) => {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;



  const systemPrompt = `You are a helpful Poultry Farm Finance & Production AI assistant.
IMPORTANT: When outputting math equations or formulas, you MUST enclose them in $$...$$ for block math or $...$ for inline math.
CRITICAL: If you use the percentage symbol '%' inside any math block ($ or $$), you MUST always escape it as '\\%'. DO NOT use an unescaped '%' inside LaTeX or KaTeX blocks, as it will cause a parsing error.`;

  let contents: any[] = [];
  let parts: any[] = [{ text: `${systemPrompt}\n\nUser Request: ${prompt}` }];

  if (files && files.length > 0) {
    const fileParts = await Promise.all(files.map(async (file) => {
      const response = await fetch(file.url);
      const buffer = await response.arrayBuffer();
      const base64 = btoa(
        new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), "")
      );
      return {
        inline_data: {
          data: base64,
          mime_type: file.mimeType
        }
      };
    }));
    parts = [...fileParts, ...parts];
  }

  contents.push({ parts });

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents })
  });

  if (!response.ok) {
    const errorBody = await response.text();
    console.error("Gemini API Error:", errorBody);
    throw new Error(`Gemini API Error: ${response.status}`);
  }

  const result = await response.json();
  return result.candidates[0].content.parts[0].text;
};

