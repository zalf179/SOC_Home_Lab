

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

