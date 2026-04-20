// api/img.js - Proxy de imágenes desde Google Drive
export default async function handler(req, res) {
  const { id } = req.query;
  if (!id || !/^[\w-]+$/.test(id)) {
    return res.status(400).json({ error: 'ID inválido' });
  }

  try {
    // Intentar con export directo de Drive
    const driveUrl = `https://drive.google.com/uc?export=view&id=${id}`;
    const response = await fetch(driveUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; ViverosTerra/1.0)',
        'Accept': 'image/jpeg,image/png,image/*',
      },
      redirect: 'follow',
    });

    if (!response.ok) {
      throw new Error(`Drive respondió ${response.status}`);
    }

    const contentType = response.headers.get('content-type') || 'image/jpeg';
    if (!contentType.startsWith('image/')) {
      throw new Error('No es imagen');
    }

    const buffer = await response.arrayBuffer();
    res.setHeader('Content-Type', contentType);
    res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=86400');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.send(Buffer.from(buffer));
  } catch (err) {
    // Fallback: thumbnail de Drive
    try {
      const thumbUrl = `https://lh3.googleusercontent.com/d/${id}=w400`;
      const r2 = await fetch(thumbUrl);
      if (r2.ok) {
        const buf = await r2.arrayBuffer();
        res.setHeader('Content-Type', 'image/jpeg');
        res.setHeader('Cache-Control', 'public, max-age=86400');
        res.send(Buffer.from(buf));
        return;
      }
    } catch {}
    res.status(404).json({ error: 'Imagen no encontrada', detail: err.message });
  }
}
