#!/usr/bin/env python3
import sys
import json
import requests
from requests.exceptions import RequestException

# Argumen: 1=Alert File Path, 2=API Key (dummy), 3=Hook URL

def send_event():
    try:
        # Menggunakan sys.argv[1] karena Wazuh memberi kita PATH FILE ALERT, bukan STDIN
        alert_file_path = sys.argv[1]
        hook_url = sys.argv[3]

        # Membaca konten alert dari file
        with open(alert_file_path, 'r') as f:
            alert_json = json.load(f)

        headers = {'Content-Type': 'application/json'}

        # Kirim data JSON mentah ke n8n
        response = requests.post(hook_url, json=alert_json, headers=headers)
        response.raise_for_status()

    except IndexError:
        # Ini terjadi jika argumen kurang
        sys.exit(1)
    except RequestException as e:
        # Jika ada error koneksi/HTTP
        sys.exit(1)
    except Exception as e:
        # Error lainnya (misalnya, file tidak ditemukan, JSON invalid)
        sys.exit(1)

if __name__ == "__main__":
    send_event()
