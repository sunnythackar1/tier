import zipfile
from pathlib import Path

# Project structure
base_path = Path("bookstore-app")
client_path = base_path / "client"
server_path = base_path / "server"

# File contents
files = {
    client_path / "Dockerfile": """\
FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
""",
    client_path / "package.json": """\
{
  "name": "bookstore-client",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "serve": "^14.2.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
""",
    server_path / "Dockerfile": """\
FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 5000
CMD ["node", "server.js"]
""",
    server_path / "package.json": """\
{
  "name": "bookstore-server",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.2"
  }
}
""",
    server_path / "server.js": """\
const express = require('express');
const app = express();
const PORT = 5000;

app.use(express.json());

app.get('/api/books', (req, res) => {
  res.json([
    { id: 1, title: "1984", author: "George Orwell", price: 10 },
    { id: 2, title: "Sapiens", author: "Yuval Noah Harari", price: 12 },
  ]);
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
""",
    base_path / "docker-compose.yml": """\
version: '3.8'

services:
  frontend:
    build: ./client
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./server
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=mongodb
    depends_on:
      - mongodb

  mongodb:
    image: mongo
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
"""
}

# Create directories and files
for path, content in files.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

# Create ZIP archive
zip_path = Path("bookstore-app.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for file in base_path.rglob("*"):
        zipf.write(file, file.relative_to(base_path.parent))

print("ZIP file created:", zip_path)
