import requests
import json
import time
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Back, Style
import random  # For randomizing count

colorama.init(autoreset=True)

def print_welcome_message():
    print(Fore.WHITE + r"""
_  _ _   _ ____ ____ _    ____ _ ____ ___  ____ ____ ___ 
|\ |  \_/  |__| |__/ |    |__| | |__/ |  \ |__/ |  | |__]
| \|   |   |  | |  \ |    |  | | |  \ |__/ |  \ |__| |         
          """)
    print(Fore.GREEN + Style.BRIGHT + "Nyari Airdrop Friends Factory")
    print(Fore.YELLOW + Style.BRIGHT + "Telegram: https://t.me/nyariairdrop")

def load_accounts():
    with open('data.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

def login_telegram(payload):
    url = "https://api.ffabrika.com/api/v1/auth/login-telegram"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    data = {"webAppData": {"payload": payload}}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['data']['accessToken']['value']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Login gagal: {str(e)}")
        return None

def get_profile(token):
    url = "https://api.ffabrika.com/api/v1/profile"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengambil profil: {str(e)}")
        return None

# Get factory details from the profile's factory ID
def get_factory_details(token, factory_id):
    url = f"https://api.ffabrika.com/api/v1/factories/{factory_id}"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengambil data pabrik: {str(e)}")
        return None

# Collect rewards from the factory
def collect_factory_rewards(token):
    url = "https://api.ffabrika.com/api/v1/factories/my/rewards/collection"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 204:
            print(Fore.GREEN + "Reward berhasil dikoleksi.")
        else:
            print(Fore.YELLOW + f"Status pengumpulan reward: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengoleksi reward: {str(e)}")

# Assign worker tasks to the factory
def assign_worker_tasks(token, task_type="longest"):
    url = "https://api.ffabrika.com/api/v1/factories/my/workers/tasks/assignment"
    headers = {
        "cookie": f"acc_uid={token}",
        "Content-Type": "application/json"
    }
    payload = {"type": task_type}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            print(Fore.GREEN + "Pekerja berhasil ditugaskan.")
        else:
            print(Fore.YELLOW + f"Status penugasan tugas: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal menetapkan tugas pekerja: {str(e)}")

def get_tasks(token):
    url = "https://api.ffabrika.com/api/v1/tasks"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengambil tugas: {str(e)}")
        return None


def get_daily_tasks(token):
    url = "https://api.ffabrika.com/api/v1/daily-tasks"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengambil tugas harian: {str(e)}")
        return None

def complete_task(token, task_id):
    url = f"https://api.ffabrika.com/api/v1/tasks/completion/{task_id}"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal menyelesaikan tugas: {str(e)}")
        return None

def complete_daily_task(token, task_id):
    url = f"https://api.ffabrika.com/api/v1/daily-tasks/completion/{task_id}"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal menyelesaikan tugas harian: {str(e)}")
        return None

def receive_daily_reward(token):
    url = "https://api.ffabrika.com/api/v1/daily-rewards/receiving"
    headers = {"cookie": f"acc_uid={token}"}
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(Fore.GREEN + "Hadiah harian berhasil diterima")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal menerima hadiah harian: {str(e)}")

# Send scores request with randomized count
def send_scores_request(token):
    url = "https://api.ffabrika.com/api/v1/scores"
    headers = {
        "Content-Type": "application/json",
        "cookie": f"acc_uid={token}"
    }
    
    count = random.randint(80, 150)
    data = {"count": count}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(Fore.GREEN + f"Taps {count} berhasil")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Gagal mengirim request: {str(e)}")
        return None


def process_account(payload):
    token = login_telegram(payload)
    if not token:
        return
    
    profile = get_profile(token)
    if not profile:
        return
    
    print(Fore.CYAN + f"Memproses akun: {profile['username']}")
    print(Fore.YELLOW + f"Nama: {profile['firstName']} {profile['lastName'] or ''}")
    print(Fore.YELLOW + f"Status: {profile['status']}")
    print(Fore.YELLOW + f"Skor total: {profile['score']['total']}")
    print(Fore.YELLOW + f"Liga: {profile['league']['name']}")
    print(Fore.YELLOW + f"Energi: {profile['energy']['balance']}/{profile['energy']['limit']}")
    print(Fore.YELLOW + f"Tugas sosial yang belum selesai: {profile['uncompletedSocialTasksQuantity']}")
    print(Fore.YELLOW + f"Tugas harian yang belum selesai: {profile['uncompletedDailyTasksQuantity']}")
    
    # Handle daily rewards
    if not profile['dailyReward']['isRewarded']:
        receive_daily_reward(token)
    else:
        print(Fore.YELLOW + "Hadiah harian sudah diterima")
    
    # Handle factory details
    factory_data = profile.get('factory')
    if factory_data:
        print(Fore.CYAN + f"Memproses pabrik ID: {factory_data['id']}")
        print(Fore.YELLOW + f"Reward yang tersedia: {factory_data['rewardCount']}")
        
        if factory_data['rewardCount'] > 0:
            collect_factory_rewards(token)
        else:
            print(Fore.YELLOW + "Tidak ada reward untuk dikoleksi.")
        
        if factory_data['isPlanted'] == False and factory_data['isDestroyed'] == False:
            assign_worker_tasks(token)
        else:
            print(Fore.YELLOW + "Pabrik tidak tersedia untuk tugas.")
    else:
        print(Fore.RED + "Tidak ada data pabrik dalam profil.")
    
    # Handle tasks and energy
    tasks = get_tasks(token)
    if tasks:
        for task in tasks:
            if not task['isCompleted']:
                result = complete_task(token, task['id'])
                if result:
                    print(Fore.GREEN + f"Tugas '{task['description']}' selesai. Reward: {task['reward']}")
    
    daily_tasks = get_daily_tasks(token)
    if daily_tasks:
        print(Fore.CYAN + "Tugas Harian:")
        for task in daily_tasks:
            print(Fore.YELLOW + f"- {task['description']}: Progress {task['progress']}/{task['goal']}, Reward: {task['reward']}")
            if not task['isCompleted'] and task['progress'] >= task['goal']:
                result = complete_daily_task(token, task['id'])
                if result:
                    print(Fore.GREEN + f"Tugas harian '{task['description']}' selesai. Reward: {task['reward']}")
    
    while profile['energy']['balance'] > 0:
        print(Fore.YELLOW + f"Sisa Energi: {profile['energy']['balance']}")
        response = send_scores_request(token)
        if response:
            profile = get_profile(token)
            if not profile:
                return
        else:
            print(Fore.RED + "Gagal mengirim request. Menghentikan loop.")
            break
    
    print(Fore.CYAN + "Energi habis, selesai memproses akun\n")


def main():
    print_welcome_message()
    accounts = load_accounts()
    total_accounts = len(accounts)
    
    print(Fore.YELLOW + f"Total akun: {total_accounts}")
    
    for i, payload in enumerate(accounts, 1):
        print(Fore.CYAN + f"Memproses akun {i} dari {total_accounts}")
        process_account(payload)
        if i < total_accounts:
            print(Fore.YELLOW + "Menunggu 5 detik sebelum akun berikutnya...")
            time.sleep(5)
    
    print(Fore.GREEN + "Semua akun telah diproses.")
    
    while True:
        target_time = datetime.now() + timedelta(days=0.01157)
        while datetime.now() < target_time:
            remaining_time = target_time - datetime.now()
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(Fore.YELLOW + f"\rWaktu tersisa: {hours:02d}:{minutes:02d}:{seconds:02d}", end="", flush=True)
            time.sleep(1)
        
        print(Fore.GREEN + "\nMemulai proses kembali...")
        main()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan: {str(e)}")
        print(Fore.YELLOW + "Melanjutkan ke tugas berikutnya...")
