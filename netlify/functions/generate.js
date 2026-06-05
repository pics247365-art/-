exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { description } = JSON.parse(event.body);

    if (!description || description.trim().length < 3) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'תיאור קצר מדי' })
      };
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-opus-4-8',
        max_tokens: 4096,
        messages: [{
          role: 'user',
          content: `אתה מומחה לעיצוב דפי נחיתה בעברית.
צור דף נחיתה מקצועי, יפה ומלא עבור: "${description}"

דרישות:
- HTML מלא עם CSS מובנה (inline בתוך <style>)
- עברית, RTL, dir="rtl"
- עיצוב מודרני וכהה — רקע #0a0a0a, טקסט #e8e0d0, הדגשות בזהב #c49a2a
- פונטים: Frank Ruhl Libre לכותרות, Assistant לגוף (Google Fonts)
- סקציות: Hero עם CTA, שירותים/יתרונות, ביקורת/המלצה, יצירת קשר
- כפתור CTA ראשי בזהב עם href="https://wa.me/972500000000"
- mobile-first, responsive
- אל תכלול JavaScript מורכב

החזר רק את קוד ה-HTML המלא, ללא הסברים, ללא markdown, ללא backticks.`
        }]
      })
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Anthropic API error:', err);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'שגיאה מה-API' })
      };
    }

    const data = await response.json();
    const html = data.content[0].text.trim();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ html })
    };

  } catch (err) {
    console.error(err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'שגיאה פנימית' })
    };
  }
};
