

---

# 🔗 Install n8n using Docker Compose

This guide explains how to deploy **n8n**, a powerful workflow automation tool, using Docker Compose.

## 🛠️ Preparation

1. **Install Docker & Docker Compose** (Ensure they are already installed on your Ubuntu server).
2. **Create a project directory**:
```bash
mkdir n8n && cd n8n

```



## 🚀 Deployment

### 1. Create the Docker Compose File

Create a `docker-compose.yml` file:

```bash
nano docker-compose.yml

```

Paste the following configuration:

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    ports:
      - "5678:5678"
    environment:
      - TZ=Asia/Jakarta
      - GENERIC_TIMEZONE=Asia/Jakarta
      - N8N_HOST=192.168.0.30
      - N8N_PORT=5678
      - N8N_SECURE_COOKIE=false
      - WEBHOOK_URL=http://192.168.0.30:5678
    volumes:
      - ./n8n_data:/home/node/.n8n
    restart: always

```

### 2. Launch n8n

Run the container in detached mode (background):

```bash
docker compose up -d

```

### 3. Verify the Container

Check if the container is running:

```bash
docker ps

```

## 🖥️ Accessing n8n

Open your web browser and navigate to:

```text
http://192.168.0.30:5678

```

## 📂 Data Persistence

All your workflows and settings are stored locally in the `./n8n_data` folder within your project directory.

---

