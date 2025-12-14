

---

## 🛡️ Installing Wazuh on Ubuntu Server 

### Prerequisites **Operating System:** Ubuntu Server (Recommended: 20.04 or 22.04 LTS).
* **Hardware Requirements:**
* **Minimum:** 4 vCPUs, 8 GB RAM, 50 GB Disk space.


* **User Access:** `sudo` privileges.

### Step 1: System Preparation and Updates Before starting, ensure your system is up-to-date and necessary dependencies are ready.

```bash
# Update package lists and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install curl (often pre-installed, but good to ensure)
sudo apt install curl -y

```

### Step 2: Running the Wazuh Installation Script.

> ⚠️ **Note:** Always check the [official Wazuh documentation](https://documentation.wazuh.com/current/quickstart.html) for the latest version number. Replace `4.x` with the desired version (e.g., `4.14`).

```bash
# 1. Download and Run installation script
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh && sudo bash ./wazuh-install.sh -a

```

Wait for the script to complete. This process may take several minutes as it downloads packages, generates security keys, and starts all services.
Once the assistant finishes the installation, the output shows the access credentials and a message that confirms that the installation was successful.
<img width="574" height="86" alt="image" src="https://github.com/user-attachments/assets/47cde0aa-a059-4bf0-96df-b235d7bdd707" />



### Step 3: Accessing the Wazuh Dashboard The Wazuh Dashboard is accessible via your server's IP address using HTTPS on the default port **443**.

* **Open your web browser** and navigate to:
```
https://<Your_Ubuntu_Server_IP_Address>

```


* **Security Warning:** You will encounter a browser warning because the installation uses self-signed certificates. Accept the risk and proceed.
* **Login:** Use the `admin` username and the password.

---


### If you miss the credentials, you can retrieve them from the generated archive file (`wazuh-install-files.tar`):


```bash
sudo tar -O -xvf wazuh-install-files.tar wazuh-install-files/wazuh-passwords.txt

```

