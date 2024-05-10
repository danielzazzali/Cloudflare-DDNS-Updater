import http.client
import json
import os
import sys
import time
from dotenv import load_dotenv


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class CloudflareDDNSUpdater:
    def __init__(self):
        load_dotenv()

        self.auth_token = os.getenv('AUTH_TOKEN')
        self.api_host = os.getenv('API_HOST')
        self.api_path = os.getenv('API_PATH')
        self.zone_id = os.getenv('ZONE_ID')
        self.proxied = str2bool(os.getenv('PROXIED'))
        self.ttl = os.getenv('TTL')

        self.headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.auth_token}"
        }

        self.conn = http.client.HTTPSConnection(self.api_host)

    def verify_token(self):
        self.conn.request("GET", f"{self.api_path}user/tokens/verify", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)

        status = json_data['result']['status']

        return status

    def get_my_ip(self):
        self.conn.request("GET", '/cdn-cgi/trace')
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        lines = data.split('\n')
        response_dict = {line.split('=')[0]: line.split('=')[1] for line in lines if '=' in line}
        actual_ip = response_dict.get('ip')

        return actual_ip

    def get_dns_records(self):
        self.conn.request("GET", f"{self.api_path}zones/{self.zone_id}/dns_records", headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)

        return json_data['result']

    def update_dns_record(self, dns_record_id, new_ip, dns_record_type, dns_record_name):
        payload = {
            "type": dns_record_type,
            "name": dns_record_name,
            "content": new_ip,
            "ttl": self.ttl,
            "proxied": self.proxied
        }
        json_payload = json.dumps(payload)

        self.conn.request("PUT", f"{self.api_path}zones/{self.zone_id}/dns_records/{dns_record_id}", body=json_payload,
                          headers=self.headers)
        res = self.conn.getresponse()
        data = res.read().decode('utf-8')
        json_data = json.loads(data)

        return json_data

    def update_all_dns_records(self):
        current_ip = self.get_my_ip()
        records = self.get_dns_records()
        updated_records = []

        for record in records:
            dns_record_id = record['id']
            dns_record_type = record['type']
            dns_record_name = record['name']
            update_result = self.update_dns_record(dns_record_id, current_ip, dns_record_type, dns_record_name)
            updated_records.append((dns_record_name, update_result))

        return updated_records


ddns_updater = CloudflareDDNSUpdater()

log_file_path = os.getenv('LOG_FILE_PATH')
log_file = open(f'{log_file_path}Cloudflare-DDNS-Updater.log', "a")

original_stdout = sys.stdout
sys.stdout = log_file

print(150*'-')
print("Execution started at: ", time.ctime())

print("\nGetting current IP...")
ip = ddns_updater.get_my_ip()
print("Current IP: ", ip)

print("\nVerifying token...")
token_status = ddns_updater.verify_token()
print("Token status: ", token_status)

print("\nGetting DNS records...")
dns_records = ddns_updater.get_dns_records()
for dns_record in dns_records:
    print("DNS Record:", dns_record)

print("\nUpdating all DNS records...")
update_results = ddns_updater.update_all_dns_records()
for record_name, result in update_results:
    print("Update result for record:", {record_name: result})

print(150*'-')

sys.stdout = original_stdout
log_file.close()
