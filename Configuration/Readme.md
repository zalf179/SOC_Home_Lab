
## 🔗 Monitoring Apache Log  

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

## 🔗 Monitoring Suricata Log 
---


To monitor Suricata alerts in your Wazuh dashboard, you must configure the Wazuh manager to read Suricata's JSON output.

### 1. Edit Wazuh manager Configuration

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




## 🛠️ Wazuh Custom Rules for Bruteforce Detection (Hydra)

To detect automated attacks, we need to create custom rules that specifically look for the **Hydra** user-agent and trigger a high-level alert when multiple attempts occur.

### 1. Edit Local Rules

On your **Wazuh Manager**, open the local rules file:

```bash
sudo nano /var/ossec/etc/rules/local_rules.xml

```

### 2. Add the Detection Rules

Copy and paste the following group configuration. This includes:

* **Rule 31108**: Overwrites the default rule to ensure Hydra is not ignored.
* **Rule 100006**: Detects the Hydra User-Agent in web logs.
* **Rule 100007**: A **frequency-based rule** that triggers a **Level 15 (Critical)** alert if the same IP performs 5 attempts within 60 seconds.

```xml
<group name="web,appsec,attack,">

  <rule id="31108" level="0" overwrite="yes">
    <if_sid>31100</if_sid>
    <match>!Hydra</match> 
    <description>Ignored URLs (simple queries) - Excluding Hydra.</description>
  </rule>

  <rule id="100006" level="12">
    <if_sid>31100</if_sid>
    <match>Mozilla/5.0 (Hydra)</match>
    <description>Hydra Tool Access detected via User-Agent (Base Rule).</description>
    <group>attack,tool_detection,</group>
  </rule>

  <rule id="100007" level="15" frequency="5" timeframe="60">
    <if_matched_sid>100006</if_matched_sid>
    <same_source_ip />
    <description>CRITICAL: Hydra Bruteforce Attack Detected.</description>
    <group>attack,bruteforce,web,high_attack_activity,</group>
  </rule>

</group>

```

### 3. Test and Restart

Check if the rules have any syntax errors and restart the manager:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
sudo systemctl restart wazuh-manager

```

## 🧪 Simulation

You can test this rule by running a Hydra attack from another machine or you can use my bruteforce.py:

```bash
python bruteforce.py

```

Once triggered, Wazuh will fire **Rule 100007**, which is automatically caught by the **n8n integration** we configured earlier.

---
























## 🔗 Wazuh to n8n Integration (Webhook)

1. Open your **n8n** dashboard.
2. Create a new workflow and add a **Webhook Node**.
3. Set the HTTP Method to `POST`.
4. Ensure to copy the Webhook path
5. Use the "Production URL" for permanent use.

---

This configuration allows the **Wazuh Manager** to send specific alerts to an **n8n webhook** for automated incident response or notifications.

### 1. Edit Wazuh Manager Configuration

On your **Wazuh Manager** server, open the configuration file:

```bash
sudo nano /var/ossec/etc/ossec.conf

```

### 2. Add the Integration Block

Paste the following block inside the `<ossec_config>` section, change the ip and webhook path that you just copy from n8n webhook node. This will trigger the webhook whenever **Rule ID 100007** is fired.

```xml
<integration>
  <name>custom-n8n</name>  
  <hook_url>http://your-ip:5678/webhook/your-path</hook_url>
  <rule_id>100007</rule_id>
  <alert_format>json</alert_format>
</integration>

```

### 3. Restart Wazuh Manager

To apply the integration, restart the manager service:

```bash
sudo systemctl restart wazuh-manager

```
Make sure the Script custom-n8n and custom-n8n.py is in /var/ossec/integrations/
