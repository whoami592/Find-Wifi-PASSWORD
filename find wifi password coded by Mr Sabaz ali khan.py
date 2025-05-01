import subprocess

def get_wifi_passwords():
    try:
        # Get all WiFi profiles
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        
        # Store results
        wifi_list = []
        
        # Get password for each profile
        for profile in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    wifi_list.append({"SSID": profile, "Password": results[0]})
                except IndexError:
                    wifi_list.append({"SSID": profile, "Password": ""})
            except subprocess.CalledProcessError:
                wifi_list.append({"SSID": profile, "Password": "ENCODING ERROR"})
        
        # Print results
        for wifi in wifi_list:
            print("{:<30}| {:<}".format(wifi["SSID"], wifi["Password"]))
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("WiFi Profiles and Passwords")
    print("-" * 50)
    get_wifi_passwords()