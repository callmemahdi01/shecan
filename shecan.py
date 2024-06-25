import subprocess
import customtkinter as ctk
from tkinter import messagebox
import webbrowser

def check_dns_status():
    try:
        query_script = '''
        $NetworkAdapterName = "Wi-Fi"
        $Profile = Get-NetIPInterface -InterfaceAlias $NetworkAdapterName
        $InterfaceIndex = $Profile.ifIndex
        $DnsServers = (Get-DnsClientServerAddress -InterfaceIndex $InterfaceIndex).ServerAddresses
        $DnsSet = ($DnsServers -eq "178.22.122.100" -and $DnsServers -eq "185.51.200.2")
        if ($DnsSet) {
            return "custom"
        } else {
            return "automatic"
        }
        '''
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", query_script], shell=False, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return "error"

def toggle_dns():
    global dns_set
    current_status = check_dns_status()
    if current_status == "custom":
        reset_dns()
        dns_set = False
        btn_toggle.configure(text="Connect")
    elif current_status == "automatic":
        set_dns()
        dns_set = True
        btn_toggle.configure(text="Disconnect")
    else:
        messagebox.showerror("Error", "Failed to determine DNS status.")

def set_dns():
    try:
        dns_script = '''
        $NetworkAdapterName = "Wi-Fi"
        $Profile = Get-NetIPInterface -InterfaceAlias $NetworkAdapterName
        $InterfaceIndex = $Profile.ifIndex
        $DnsClientServerAddress = "178.22.122.100","185.51.200.2"
        Set-DnsClientServerAddress -InterfaceIndex $InterfaceIndex -ServerAddresses $DnsClientServerAddress
        '''
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", dns_script], shell=False)
        lbl_status.configure(text="Connected to\n185.51.200.21\n78.22.122.100", text_color="#62b5fc")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def reset_dns():
    try:
        reset_script = '''
        $NetworkAdapterName = "Wi-Fi"
        Set-DnsClientServerAddress -InterfaceIndex (Get-NetIPInterface -InterfaceAlias $NetworkAdapterName).ifIndex -ResetServerAddresses
        '''
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", reset_script], shell=False)
        lbl_status.configure(text="DNS: Automatic (DHCP)", text_color="#b0ccff")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Initialize dns_set based on current DNS status
dns_set = check_dns_status() == "custom"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("DNS Changer")
root.geometry("300x200")

btn_toggle = ctk.CTkButton(root, text="Connect" if not dns_set else "Disconnect", command=toggle_dns)
btn_toggle.pack(pady=20)

def open_github(event):
    webbrowser.open_new("https://github.com/callmemahdi01")

lbl_github = ctk.CTkLabel(root, text="click to open github", text_color="#616161", font=("x", 10))
lbl_github.pack(side="bottom", pady=(0, 5))

lbl_github.bind("<Enter>", lambda event: lbl_github.configure(text_color="#62b5fc"))
lbl_github.bind("<Leave>", lambda event: lbl_github.configure(text_color="#616161"))
lbl_github.bind("<Button-1>", open_github)

lbl_created_by = ctk.CTkLabel(root, text="created by Mahdi", text_color="#616161", font=("x", 15))
lbl_created_by.pack(side="bottom")

lbl_status = ctk.CTkLabel(root, text="", text_color="black", font=("x", 12))
lbl_status.pack()

root.mainloop()
