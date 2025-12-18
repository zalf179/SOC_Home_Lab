# Automated Threat Response: From Apache Log to Firewall Block using Wazuh, n8n, and VirusTotal


---

## This project outlines the implementation of a lightweight, adaptive Security Operations Center (SOC) workflow designed for real-time threat monitoring and automated response on a single Ubuntu server.

The core goal is to minimize the time between a potential intrusion attempt (detected via suspicious Apache web access logs) and the mitigation of the threat (blocking the malicious IP address via Iptables).

The solution utilizes a powerful stack:

1. **Wazuh:** Acts as the Security Information and Event Management (SIEM) tool, collecting Apache access logs and generating high-fidelity alerts based on predefined rules (e.g., repeated login failures, unusual access patterns).
2. **n8n:** Serves as the Security Orchestration, Automation, and Response (SOAR) engine, triggered by Wazuh webhooks.
3. **VirusTotal (VT):** Provides external Threat Intelligence (TI) for enriching the alert data, verifying if the source IP is known to be malicious.
4. **Iptables:** Executes the final automated block command based on the n8n logic.

This setup transforms manual incident handling into a fully automated, *set-it-and-forget-it* defense mechanism.

---

### 📋 Requirements & Technology StackThis project requires a single Ubuntu Server instance with sufficient resources and the following components installed and configured:

| Component | Role | Status |
| --- | --- | --- |
| **Ubuntu Server (20.04/22.04)** | Operating System | OS |
| **Wazuh** | SIEM & Log Analysis | Required |
| **Suricata** | Network Intrusion Detection System (NIDS) | Required |
| **Apache2** | Web Server (Source of Monitored Logs) | Required |
| **n8n** | Automation/SOAR Engine | Required |
| **VirusTotal API Key** | Threat Intelligence Enrichment | Required |
| **Iptables** | Host Firewall for Blocking | Built-in |

---

### 🛠️ Installation Order For a smooth setup, follow this logical installation sequence:

#### 1. Wazuh Installation The foundational SIEM layer. This includes the Manager, Indexer, and Dashboard.

#### 2. Apache Installation Install the web server whose logs will be monitored by Wazuh.

#### 3. Suricata Installation Install the NIDS component to provide network-level insights and alerts.

#### 4. n8n Installation Install the workflow automation engine. This will integrate with Wazuh and VirusTotal.

#### 5. Configuration & Integration This phase involves:

* Configuring Wazuh to ingest Apache and Suricata logs.
* Creating Wazuh Rules/Decoders for specific threats.
* Setting up the n8n workflow triggered by the Wazuh webhook.
* Integrating the VirusTotal API key into the n8n workflow.
