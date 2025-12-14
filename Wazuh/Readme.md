

---

## 🛡️ Installing Wazuh on Ubuntu ServerThis guide provides the steps to set up the complete Wazuh platform (Wazuh Manager, Wazuh Indexer, and Wazuh Dashboard) on a single Ubuntu Server instance using the recommended **Wazuh Installation Assistant**.

### Prerequisites* **Operating System:** Ubuntu Server (Recommended: 20.04 or 22.04 LTS).
* **Hardware Requirements:**
* **Minimum:** 4 vCPUs, 8 GB RAM, 50 GB Disk space.


* **User Access:** `sudo` privileges.

### Step 1: System Preparation and UpdatesBefore starting, ensure your system is up-to-date and necessary dependencies are ready.

```bash
# Update package lists and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install curl (often pre-installed, but good to ensure)
sudo apt install curl -y

# (Optional, but Recommended) Set the correct timezone
sudo dpkg-reconfigure tzdata

```

### Step 2: Running the Wazuh Installation AssistantWazuh provides a streamlined installation script that handles all component installations (Wazuh Indexer, Wazuh Manager, and Wazuh Dashboard), certificate creation, and service configuration.

> ⚠️ **Note:** Always check the [official Wazuh documentation](https://documentation.wazuh.com/current/quickstart.html) for the latest version number. Replace `4.x` with the desired version (e.g., `4.9`).

```bash
# 1. Download the installation script
curl -sO https://packages.wazuh.com/4.x/wazuh-install.sh

# 2. Run the script with the '-a' flag to install ALL components (all-in-one setup)
sudo bash ./wazuh-install.sh -a

```

Wait for the script to complete. This process may take several minutes as it downloads packages, generates security keys, and starts all services.

### Step 3: Secure Your Access Credentials Upon successful completion, the script will output the necessary **admin credentials** for the Wazuh Dashboard.

> 🔥 **CRITICAL:** **SAVE THESE CREDENTIALS IMMEDIATELY.** You will need them to log into the Dashboard.

* If you miss the credentials, you can retrieve them from the generated archive file (`wazuh-install-files.tar`):

```bash
sudo tar -O -xvf wazuh-install-files.tar wazuh-install-files/wazuh-passwords.txt

```

### Step 4: Accessing the Wazuh Dashboard The Wazuh Dashboard is accessible via your server's IP address using HTTPS on the default port **443**.

* **Open your web browser** and navigate to:
```
https://<Your_Ubuntu_Server_IP_Address>

```


* **Security Warning:** You will encounter a browser warning because the installation uses self-signed certificates. Accept the risk and proceed.
* **Login:** Use the `admin` username and the password you saved in Step 3.

---

## ➡️ Next Steps: Deploying AgentsOnce your Wazuh Platform is operational, you need to deploy **Wazuh Agents** on the endpoints (servers, workstations) you wish to monitor.

1. Navigate to the Dashboard.
2. Go to **Wazuh** \rightarrow **Server Management** \rightarrow **Deploy new agent**.
3. Select the **Operating System** of your target endpoint.
4. Follow the instructions provided by the Dashboard, ensuring you use the correct IP address for your Wazuh Server.

---
