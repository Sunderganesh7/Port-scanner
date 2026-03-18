import socket
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

COMMON_PORTS = {21:'FTP',22:'SSH',80:'HTTP',443:'HTTPS'}

class PortScanner:
    def __init__(self, target, start, end):
        self.target = target
        self.start = start
        self.end = end
        self.queue = queue.Queue()
        self.stop_flag = False
        self.total = end - start + 1
        self.scanned = 0

    def scan(self, port):
        if self.stop_flag:
            return
        try:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((self.target, port)) == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                self.queue.put(("OPEN", f"Port {port} ({service}) OPEN"))
            s.close()
        except:
            pass
        finally:
            self.scanned += 1
            self.queue.put(("PROGRESS", self.scanned, self.total))

    def start_scan(self):
        for port in range(self.start, self.end + 1):
            if self.stop_flag:
                break
            threading.Thread(target=self.scan, args=(port,), daemon=True).start()
        self.queue.put(("DONE",))


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner")
        self.root.geometry("850x550")
        self.root.configure(bg="#0f172a")

        self.build_ui()

    def build_ui(self):
        # Header
        tk.Label(self.root, text="Network Port Scanner",
                 font=("Segoe UI", 18, "bold"),
                 bg="#0f172a", fg="#38bdf8").pack(pady=10)

        # Card Frame
        card = tk.Frame(self.root, bg="#1e293b", padx=20, pady=15)
        card.pack(pady=10)

        tk.Label(card, text="Target", bg="#1e293b", fg="#e2e8f0").grid(row=0, column=0)
        self.target = tk.Entry(card, width=25)
        self.target.grid(row=0, column=1, pady=5)

        tk.Label(card, text="Start Port", bg="#1e293b", fg="#e2e8f0").grid(row=1, column=0)
        self.start = tk.Entry(card)
        self.start.insert(0, "1")
        self.start.grid(row=1, column=1)

        tk.Label(card, text="End Port", bg="#1e293b", fg="#e2e8f0").grid(row=2, column=0)
        self.end = tk.Entry(card)
        self.end.insert(0, "1024")
        self.end.grid(row=2, column=1)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack()

        def btn(text, cmd):
            return tk.Button(btn_frame, text=text, command=cmd,
                             bg="#38bdf8", fg="black",
                             font=("Segoe UI", 10, "bold"),
                             width=10)

        btn("Start", self.start_scan).grid(row=0, column=0, padx=5)
        btn("Stop", self.stop_scan).grid(row=0, column=1, padx=5)
        btn("Clear", self.clear).grid(row=0, column=2, padx=5)
        btn("Save", self.save).grid(row=0, column=3, padx=5)

        # Progress
        self.progress = ttk.Progressbar(self.root, length=600)
        self.progress.pack(pady=10)

        self.status = tk.Label(self.root, text="Status: Idle",
                               bg="#0f172a", fg="#e2e8f0")
        self.status.pack()

        # Output
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output = tk.Text(frame, bg="#020617", fg="#22c55e",
                              font=("Consolas", 10))
        self.output.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.output.yview)
        scrollbar.pack(side="right", fill="y")
        self.output.config(yscrollcommand=scrollbar.set)

    def start_scan(self):
        try:
            ip = socket.gethostbyname(self.target.get())
            start = int(self.start.get())
            end = int(self.end.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Scanning {ip}...\n\n")

        self.scanner = PortScanner(ip, start, end)
        threading.Thread(target=self.scanner.start_scan, daemon=True).start()
        self.update()

    def stop_scan(self):
        if hasattr(self, 'scanner'):
            self.scanner.stop_flag = True

    def clear(self):
        self.output.delete(1.0, tk.END)
        self.progress['value'] = 0

    def save(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, "w") as f:
                f.write(self.output.get(1.0, tk.END))

    def update(self):
        try:
            while True:
                msg = self.scanner.queue.get_nowait()

                if msg[0] == "OPEN":
                    self.output.insert(tk.END, msg[1] + "\n")

                elif msg[0] == "PROGRESS":
                    percent = int((msg[1] / msg[2]) * 100)
                    self.progress['value'] = percent
                    self.status.config(text=f"Scanning... {percent}%")

                elif msg[0] == "DONE":
                    self.status.config(text="Completed")
                    return

        except:
            pass

        self.root.after(100, self.update)


root = tk.Tk()
App(root)
root.mainloop()