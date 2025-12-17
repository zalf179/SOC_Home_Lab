

To monitor Apache access logs using Wazuh , you need to add the log location to your manager configuration.

### 1. Edit Configuration

Open the Wazuh/OSSEC configuration file:

```bash
sudo nano /var/var/ossec/etc/ossec.conf

```

### 2. Add Log Source

Find the `<!-- Log analysis -->` section and paste the following block:

```xml
  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/apache2/access.log</location>
  </localfile>

```

### 3. Restart Service

Apply the changes by restarting the Wazuh/OSSEC manager or agent:

```bash
sudo systemctl restart wazuh-manager.service

```

---


To monitor Suricata alerts in your Wazuh dashboard, you must configure the Wazuh manager to read Suricata's JSON output.

### 1. Edit Wazuh Agent Configuration

Open the `ossec.conf` file:

```bash
sudo nano /var/ossec/etc/ossec.conf

```

### 2. Add Suricata Log Source

add the following block in the end of file to monitor the `eve.json` file:

```xml
<ossec_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</ossec_config>

```

### 3. Restart Wazuh manager

Apply the new configuration by restarting the service:

```bash
sudo systemctl restart wazuh-manager

```

### 4. Verify Integration

<img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/afde3017-0afa-4537-95cb-5cd8282fcdec" />

This is the example of suricata alert log in wazuh
---
