import Busboy from 'busboy';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: false, // Disable Next.js default body parsing
  },
};

export async function POST(req) {
  console.log('request:', req);
  const uploadDir = path.join(process.cwd(), 'public/uploads');

  // Ensure the upload directory exists
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
  }

  return new Promise((resolve, reject) => {
    try {
      const busboy = Busboy({ headers: req.headers });

      let filePath;
      busboy.on('file', (fieldname, file, filename) => {
        filePath = path.join(uploadDir, filename);
        const writeStream = fs.createWriteStream(filePath);
        file.pipe(writeStream);
      });

      busboy.on('finish', () => {
        resolve(
          new Response(
            JSON.stringify({
              message: 'File uploaded successfully',
              path: `/uploads/${path.basename(filePath)}`,
            }),
            { status: 200, headers: { 'Content-Type': 'application/json' } }
          )
        );
      });

      busboy.on('error', (err) => {
        console.error('Busboy error:', err);
        reject(
          new Response(
            JSON.stringify({ message: 'Error uploading file' }),
            { status: 500, headers: { 'Content-Type': 'application/json' } }
          )
        );
      });

      req.pipe(busboy);
    } catch (error) {
      console.error('Unexpected error:', error);
      reject(
        new Response(
          JSON.stringify({ message: 'Unexpected server error' }),
          { status: 500, headers: { 'Content-Type': 'application/json' } }
        )
      );
    }
  });
}
