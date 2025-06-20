import requests
import time

def make_api_call():
    url = 'https://tlb.fly.dev/v1/login'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "email": "ogbanugot@gmail.com",
        "password": "mypass258"
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=300)  # 5-minute timeout
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except requests.Timeout:
        print("Request timed out after 5 minutes.")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        make_api_call()
        print("Waiting 3 days before making the next API call...")
        time.sleep(3 * 24 * 60 * 60)  # Sleep for 5 days

if __name__ == "__main__":
    main()

