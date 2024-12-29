# Datal-Genes
```plaintext
  ____        _        _    ____                       
 |  _ \  __ _| |_ __ _| |  / ___| ___ _ __   ___  ___  
 | | | |/ _` | __/ _` | | | |  _ / _ \ '_ \ / _ \/ __| 
 | |_| | (_| | || (_| | | | |_| |  __/ | | |  __/\__ \ 
 |____/ \__,_|\__\__,_|_|  \____|\___|_| |_|\___||___/ 
        Enhanced AutoRecon Tool
```

This tool is designed to enhance and simplify the use of AutoRecon, a reconnaissance tool for penetration testing. It integrates a Flask-based web server to visualize scan results and provides a modern interface with easy navigation.

---

## Features

- **Secure Access:** Password-protected access ensures only authorized users can operate the tool.
- **AutoRecon Integration:** Automatically organizes AutoRecon results for easy access.
- **Web Interface:** View and navigate reports using a Bootstrap-powered modern web interface.
- **Dynamic Updates:** Automatically detects new reports and updates the web interface accordingly.
- **Flask Framework:** A lightweight web server for serving files and rendering templates.

---

## Installation

### Prerequisites

1. **Python 3.7+**
2. **pip**
3. **Flask** and **Rich** Python libraries:

   ```bash
   pip install flask rich
   ```

4. AutoRecon installed and configured in your environment.

### Setup

1. Clone or download the repository.
2. Ensure the `results` directory exists in the same location as the script or is created during AutoRecon scans.
3. Place the script (`Datal-Genes.py`) and its templates in the working directory.

---

## Usage

1. **Run the Script:**

   ```bash
   python Datal-Genes.py
   ```

2. **Login:** Enter the correct password to access the tool.

3. **Main Menu Options:**
   - Run a new AutoRecon scan.
   - Start the web server to view results.
   - Exit the tool.

4. **Web Interface:**
   - Start the web server from the menu.
   - Open a browser and navigate to `http://127.0.0.1:5000`.

---

## Web Interface

### Features
- **Folder View:** Organized display of AutoRecon results grouped by IP address.
- **File View:** Clickable links to open specific files.
- **No Results Page:** Informative page when no reports are available.

### Templates
The tool dynamically generates HTML templates stored in a `templates` directory:
- `index.html`: Displays available reports.
- `no_reports.html`: Displays when no reports are found.

---

## Configuration

### Modify Password
To change the password, update the `PASSWORD` variable in the script:

```python
PASSWORD = "your_new_password"
```

### Customize Report Directory
Set a custom directory for reports by changing the `REPORT_DIR` constant:

```python
REPORT_DIR = "your_directory_name"
```

---

## Credits

- **AutoRecon**: The primary scanning tool integrated.
- **Flask**: For the lightweight web server.
- **Rich**: For enhanced console UI.

---

## Disclaimer
This tool is for educational and authorized penetration testing purposes only. Unauthorized use of this tool is prohibited and may violate laws.
