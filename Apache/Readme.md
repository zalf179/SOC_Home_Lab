
---

# 🌐 Simple Apache Web Server Setup on Ubuntu

A quick guide to installing and running the Apache HTTP Server on Ubuntu.

## 🚀 Quick Start

### 1. Install Apache

Update your package list and install the Apache2 package.

```bash
sudo apt update
sudo apt install apache2 -y

```

### 2. Configure Firewall

Allow web traffic through the firewall.

```bash
sudo ufw allow 'Apache'

```

### 3. Manage the Service

Check if Apache is running correctly.

```bash
sudo systemctl status apache2

```

* **Start:** `sudo systemctl start apache2`
* **Restart:** `sudo systemctl restart apache2`
* **Enable on boot:** `sudo systemctl enable apache2`

## 📂 Web Files & Logs

* **Web Root:** `/var/www/html/` (Put your `index.html` here)
* **Main Config:** `/etc/apache2/apache2.conf`
* **Error Logs:** `/var/log/apache2/error.log`
* **Access Logs:** `/var/log/apache2/access.log`

## 🔍 Verification

Open your browser and type your server IP:

```text
http://your_server_ip

```

If you see the **Apache2 Ubuntu Default Page**, it works!

---
