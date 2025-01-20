
import requests
from requests.auth import HTTPBasicAuth

# api
OPNSENSE_API_KEY = 'KfEzQ02Zkt/wVS6uCiqNn4Ht4+zzzzzzzzzzzzzzzzzz'
OPNSENSE_API_SECRET = 'd0AdIMgsDuCVT3VXAt1WMhBbSzzspFusGrM//zzzzzzzzzzzzzzzzzz'
OPNSENSE_API_URL = 'http://192.168.100.123/api/diagnostics/system/systemTime/loadavg'

# token telegram
TELEGRAM_BOT_TOKEN = '6220:AAE43iQbmCn_zzzzzzzzzzzzzzzzzz'
TELEGRAM_CHAT_ID = '-667zzzz'

# mengirim pesan ke Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot6220566441:AAE43iQbmCn_EMKB6lReOZGFOX8zsC-OjYs/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response

# mendapatkan load
def get_cpu_load():
    response = requests.get(OPNSENSE_API_URL, auth=HTTPBasicAuth(OPNSENSE_API_KEY, OPNSENSE_API_SECRET), verify=False)

    if response.status_code == 200:
        data = response.json()
        loadavg = data['loadavg']  # Mendapatkan nilai loadavg
        load_1min = float(loadavg.split(",")[0].strip())  # Ambil nilai load untuk 1 menit pertama
        return load_1min
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# alert jika di atas 50%
def check_cpu_load():
    cpu_load = get_cpu_load()

    if cpu_load is not None:
        print(f"CPU Load 1 menit saat ini: {cpu_load}")

        if cpu_load > 0.50:
            message = f"⚠️ Alert: CPU Load OPNsense melebihi batas! Saat ini: {cpu_load*1:.2f}%"
            send_telegram_alert(message)
            print("Alert dikirim ke Telegram!")
        else:
            print("CPU Load normal.")
    else:
        print("Gagal mendapatkan data CPU load.")

# Menjalankan fungsi
if __name__ == "__main__":
    check_cpu_load()

