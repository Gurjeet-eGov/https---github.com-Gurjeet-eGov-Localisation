import json
import subprocess
import tempfile
import os

# Constants
JSON_FILE = 'output_json/test_output_output.json'
BATCH_SIZE = 1000
ENDPOINT = 'http://localhost:8083/pt-calculator-v2/billingslab/mutation/_create'

# Static RequestInfo
REQUEST_INFO = {
    "authToken": "123",
    "userInfo": {
        "id": 96,
        "uuid": "1f-a135-4757075c5c27",
        "userName": "SUPEU",
        "name": "SUPER",
        "mobileNumber": "999995",
        "emailId": None,
        "locale": None,
        "type": "EMPLOYEE",
        "roles": [
            {"name": "HRMS Admin", "code": "HRMS_ADMIN", "tenantId": "pg.citya"}
        ],
        "active": True,
        "tenantId": "pg.citya",
        "permanentCity": None
    }
}

def send_batch(batch, index):
    payload = {
        "RequestInfo": REQUEST_INFO,
        "MutationBillingSlab": batch
    }

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
        json.dump(payload, temp_file)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            [
                "curl", "--location", ENDPOINT,
                "--header", "Content-Type: application/json",
                "--data", f"@{temp_file_path}"
            ],
            capture_output=True,
            text=True
        )

        print(f"Batch {index}: Return Code = {result.returncode}")
        if result.stdout:
            print(f"Batch {index} Response:\n{result.stdout}")
        if result.stderr:
            print(f"Batch {index} Error:\n{result.stderr}")

    finally:
        os.remove(temp_file_path)

def main():
    with open(JSON_FILE, 'r') as f:
        billing_slabs = json.load(f)

    total = len(billing_slabs)
    print(f"Total BillingSlabs: {total}")

    for i in range(0, total, BATCH_SIZE):
        batch = billing_slabs[i:i + BATCH_SIZE]
        batch_index = (i // BATCH_SIZE) + 1
        print(f"\nSending batch {batch_index} with {len(batch)} records...")
        send_batch(batch, batch_index)

if __name__ == "__main__":
    main()
