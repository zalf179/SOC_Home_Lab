
---

# 🛡️ Suricata Installation and Basic Configuration on Ubuntu Server.

Suricata functions as a powerful Intrusion Detection System (IDS), Intrusion Prevention System (IPS), and Network Security Monitoring (NSM) engine.

## Prerequisites An Ubuntu Server (tested on recent LTS versions).
* Root or `sudo` access.
* An active network connection.

## 🚀 Installation Steps
### 1. Update System Repositories 
Start by ensuring your system repositories and packages are up-to-date.

```bash
sudo apt-get update && sudo apt-get upgrade -y

```

### 2. Install Suricata Prerequisites 
Install the necessary libraries for Suricata, especially those related to network filtering and JSON processing (`jq`).

```bash
sudo apt -y install libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev libnfnetlink0 jq

```

### 3. Add the Suricata Repository (PPA) To ensure you install the latest stable version of Suricata, add the official OISF Personal Package Archive (PPA).

```bash
sudo add-apt-repository ppa:oisf/suricata-stable

```

You will be prompted to press `ENTER` to confirm adding the repository.

### 4. Install Suricata Install the main Suricata package.

```bash
sudo apt install suricata -y

```

### 5. Manage Suricata Service Enable the service to start at boot and check its initial status.

```bash
# Enable the service
sudo systemctl enable suricata

# Check initial status
sudo systemctl status suricata

```

> **Note:** The status will likely show as `active (exited)` initially because Suricata needs proper configuration (which interface to monitor) before it can run continuously.

## ⚙️ Configuration
### 1. Stop Suricata Service Before editing the configuration file, stop the Suricata service.

```bash
sudo systemctl stop suricata

```

### 2. Edit `suricata.yaml`Open the main configuration file for editing.

```bash
sudo nano /etc/suricata/suricata.yaml

```

#### A. Set `HOME_NET`
Navigate to the `HOME_NET` variable and replace the default IP range with the IP address of your Ubuntu server. This defines your protected network.

```yaml
# Replace this line:
# HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"

# With your specific IP, for example:
HOME_NET: "['YOUR_UBUNTU_IP_ADDRESS']" 

```

#### B. Set Network Interface
Use `CTRL + W` in `nano` and search for `"interface"`. Set the value to the network interface name used by your Ubuntu server (e.g., `eth0`, `ens18`, or `enp0s3`).

```yaml
# Find the interface section and update:
interface: your_interface_name 
# (e.g., interface: eth0)

```

Save and exit the file (`CTRL + O`, then `ENTER`, then `CTRL + X`).

## 3. Rule Management Suricata uses rules to detect threats. The official Suricata tools make it easy to manage them.

### A. List Available Rule Source
sSee which rule sources are available to enable.

```bash
sudo suricata-update list-sources

```

> **⚠️ Important Note:** Review the license information. You **cannot** enable sources that have a **`License: Commercial`** designation unless you have purchased the corresponding license.

### B. Enable a Rule Source, open-source rule set, such as the Emerging Threats Open rules (`et/open`).

```bash
sudo suricata-update enable-source et/open

```

### C. Update and Download Rules Apply the changes and download the newly enabled rules.

```bash
sudo suricata-update

```

## 🛠️ Testing and Running Suricata
### 1. Test Configuration Run a test to ensure your `suricata.yaml` configuration and rules are valid before starting the service.

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml -v

```

If the test is successful, you will see output indicating that the configuration is ready.

### 2. Start Suricata
Start the Suricata service to begin network monitoring.

```bash
sudo systemctl start suricata

```

### 3. Verify Running Status Check the status again; it should now show as `active (running)`.

```bash
sudo systemctl status suricata

```

## 🔍 Log Verification (Testing IDS Functionality)To confirm Suricata is actively detecting traffic based on its rules, you can use a known test signature.

### 1. Generate a Test Alert Run the following command to generate traffic that is specifically designed to trigger a standard IDS alert (known as the EICAR test for IDS/IPS).

```bash
curl http://testmynids.org/uid/index.html

```

### 2. Review Logs
Suricata's log files are located in `/var/log/suricata/`.

* **`eve.json`**: Detailed, structured log file (JSON format) for integration with log analysis tools (e.g., Splunk, ELK Stack).
* **`fast.log`**: A simple, human-readable summary of high-priority alerts.

Review the `fast.log` to see the generated alert:

```bash
sudo cat /var/log/suricata/fast.log

```

You should see an entry similar to:

```
<Timestamp>  [**] [1:2100000:7] GPL ATTACK_RESPONSE id check returned root [**] [Classification: Potentially Bad Traffic] [Priority: 2] {TCP} <Source_IP>:<Source_Port> -> <Target_IP>:<Target_Port>

```

If you see this log entry, your Suricata installation is working and detecting threats as expected!

---

