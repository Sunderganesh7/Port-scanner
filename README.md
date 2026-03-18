# 🔍 Network Port Scanner (GUI-Based)

## 📌 Overview

This project is a **GUI-based Network Port Scanner** developed using Python.
It allows users to scan a target system (IP address or hostname) and identify **open ports** within a given range.

The application uses **socket programming and multithreading** to perform fast and efficient port scanning, with a clean and user-friendly interface.

---

## 🚀 Features

* Scan any IP address or hostname
* Detect open ports in a given range
* Multithreaded scanning (fast performance)
* Real-time progress updates
* Modern GUI (dark theme)
* Save scan results to file
* Clear and user-friendly interface

---

## 🛠️ Technologies Used

* Python
* Tkinter (GUI)
* Socket Programming
* Multithreading

---

## 📂 Project Structure

```
port_scanner.py   # Main application file
README.md         # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/port-scanner.git
cd port-scanner
```

### 2. Install dependencies

Tkinter comes pre-installed with Python.
If not:

```
pip install tk
```

---

## ▶️ Usage

Run the application:

```
python port_scanner.py
```

### Input:

* **Target** → IP address or hostname (e.g., `127.0.0.1`)
* **Start Port** → Starting port number
* **End Port** → Ending port number

### Output:

* Displays list of open ports
* Shows scanning progress
* Option to save results

---

## 📸 Example

```
Scanning 127.0.0.1...

Port 80 (HTTP) OPEN
Port 443 (HTTPS) OPEN

Scan Completed
```

---

## ⚠️ Disclaimer

This tool is intended for **educational and ethical purposes only**.
Do not scan unauthorized systems without permission.

---

## 🎯 Future Enhancements

* IP range scanning
* Banner grabbing
* Export to CSV/JSON
* Advanced UI improvements

---

## 👨‍💻 Author

**Sunderganesh Yadavar**



Give it a star ⭐ on GitHub!
