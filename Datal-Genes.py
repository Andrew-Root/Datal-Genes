import os
import subprocess
import getpass
from flask import Flask, render_template, send_from_directory, url_for
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

# Console setup
console = Console()

# Constants
REPORT_DIR = "results"  # Directory where AutoRecon saves reports
PASSWORD = "securepass"  # Change this to a hashed password in production

# Flask setup
app = Flask(__name__)

@app.route("/")
def home():
    """Serve the list of available AutoRecon reports."""
    if not os.path.exists(REPORT_DIR):
        return render_template("no_reports.html")

    reports = []
    for root, dirs, files in os.walk(REPORT_DIR):
        rel_path = os.path.relpath(root, REPORT_DIR)
        if rel_path == ".":
            folder_name = "Root Directory"
        else:
            folder_name = rel_path

        folder_files = [
            {
                "name": file,
                "path": os.path.join(rel_path, file)
            } for file in files
        ]

        reports.append({
            "folder": folder_name,
            "files": folder_files
        })

    return render_template("index.html", reports=reports)

@app.route("/reports/<path:filename>")
def serve_report(filename):
    """Serve a specific report file."""
    directory = os.path.join(os.getcwd(), REPORT_DIR)
    return send_from_directory(directory, filename)

def run_autorecon(target, nmap_timing, ports):
    """Run AutoRecon and save results to the reports directory."""
    command = f"env PATH=$PATH autorecon {target} --nmap {nmap_timing} --ports {ports}"
    console.print(f"[blue]Running AutoRecon with command:[/blue] {command}")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    for line in process.stdout:
        console.print(line.strip(), style="cyan")

    process.wait()

    if process.returncode == 0:
        console.print("[green]Scan completed![/green]")
    else:
        console.print("[red]Error during the scan.[/red]")

def main():
    # Display ASCII art logo
    console.print(Text.from_markup(
        r"""[bold blue]
  ____        _        _    ____                       
 |  _ \  __ _| |_ __ _| |  / ___| ___ _ __   ___  ___  
 | | | |/ _` | __/ _` | | | |  _ / _ \ '_ \ / _ \/ __| 
 | |_| | (_| | || (_| | | | |_| |  __/ | | |  __/\__ \ 
 |____/ \__,_|\__\__,_|_|  \____|\___|_| |_|\___||___/ 
        Enhanced AutoRecon Tool
        """
    ))

    # Password check
    password = getpass.getpass("Enter password: ")
    if password != PASSWORD:
        console.print("[red]Invalid password![red]")
        return

    # Menu loop
    while True:
        console.print("\n[bold yellow]Main Menu[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="dim")
        table.add_column("Description")
        table.add_row("1", "Run an AutoRecon scan")
        table.add_row("2", "Start the web server for viewing results")
        table.add_row("3", "Exit")
        console.print(table)

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

        if choice == "1":
            target = Prompt.ask("Enter target (IP or hostname)")
            nmap_timing = Prompt.ask("Enter Nmap timing template (T1-T5)", default="T4")
            ports = Prompt.ask("Enter ports to scan (e.g., 80,443 or range 1-1000)", default="1-65535")
            run_autorecon(target, nmap_timing, ports)
        elif choice == "2":
            console.print("[green]Starting web server at http://127.0.0.1:5000[/green]")
            app.run(host="0.0.0.0", port=5000, debug=False)
        elif choice == "3":
            console.print("[bold green]Goodbye![bold green]")
            break

if __name__ == "__main__":
    # Ensure templates directory exists
    if not os.path.exists("templates"):
        os.makedirs("templates")

    # Save the HTML templates
    with open("templates/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoRecon Reports</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-primary mb-4">AutoRecon Reports</h1>
        {% for report in reports %}
            <div class="card mb-3">
                <div class="card-header bg-primary text-white">
                    {{ report.folder }}
                </div>
                <ul class="list-group list-group-flush">
                    {% for file in report.files %}
                        <li class="list-group-item">
                            <a href="{{ url_for('serve_report', filename=file.path) }}" target="_blank">{{ file.name }}</a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        {% endfor %}
    </div>
</body>
</html>
""")

    with open("templates/no_reports.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No Reports Found</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5 text-center">
        <h1 class="text-danger">No Reports Found</h1>
        <p class="text-muted">Run a scan to generate reports.</p>
    </div>
</body>
</html>
""")

    main()
