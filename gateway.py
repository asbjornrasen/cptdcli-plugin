# cptd_tools/commands/gateway.py

from colorama import Fore, Style, init
from cptd_tools.syntax_utils import print_help
import subprocess
import sys

init(autoreset=True)

SYNTAX = {
    "name": "gateway",
    "description": "Display active gateways and open ports on Linux systems. Supports filters and export.",
    "usage": "cptd gateway [options]",
    "arguments": [
        {"name": "--all", "required": False, "help": "Show all available routes."},
        {"name": "--only-gateway", "required": False, "help": "Only gateway info (no ports)."},
        {"name": "--only-ports", "required": False, "help": "Only open ports (no gateway)."},
        {"name": "--tcp", "required": False, "help": "Show only TCP ports."},
        {"name": "--udp", "required": False, "help": "Show only UDP ports."},
        {"name": "--save <file>", "required": False, "help": "Export result to file."}
    ],
    "examples": [
        "cptd gateway",
        "cptd gateway --all",
        "cptd gateway --only-gateway",
        "cptd gateway --only-ports --udp",
        "cptd gateway --tcp --save report.txt"
    ]
}

def run(argv):
    if "--help" in argv or "-h" in argv:
        print_help(SYNTAX)
        return

    if "--only-gateway" in argv and "--only-ports" in argv:
        print(Fore.RED + "[!] Error: --only-gateway and --only-ports cannot be used together." + Style.RESET_ALL)
        return

    if "--only-gateway" in argv and ("--tcp" in argv or "--udp" in argv):
        print(Fore.RED + "[!] Error: --only-gateway cannot be combined with --tcp or --udp." + Style.RESET_ALL)
        return

    show_routes = "--only-ports" not in argv
    show_ports = "--only-gateway" not in argv
    save_file = None
    output_lines = []

    if "--save" in argv:
        try:
            save_index = argv.index("--save")
            save_file = argv[save_index + 1]
        except IndexError:
            print(Fore.RED + "[!] Error: --save requires a file name." + Style.RESET_ALL)
            return

    # ───────────── GATEWAYS ─────────────
    if show_routes:
        try:
            route_output = subprocess.check_output(["ip", "route"], stderr=subprocess.STDOUT).decode()
        except Exception as e:
            route_output = f"[!] Error retrieving route: {e}"

        default_routes = []
        other_routes = []

        for line in route_output.strip().splitlines():
            if line.startswith("default"):
                default_routes.append(line)
            else:
                other_routes.append(line)

        output_lines.append(Fore.CYAN + "🌐 GATEWAY INFORMATION\n")
        if default_routes:
            output_lines.append(Fore.GREEN + "🔹 Default Gateway:")
            for route in default_routes:
                parts = route.split()
                gw = parts[2] if "via" in parts else "?"
                iface = parts[4] if "dev" in parts else "?"
                output_lines.append(f"  ➤ Gateway: {gw}  | Interface: {iface}")
        else:
            output_lines.append("🔹 Default Gateway: Not Found")

        if "--all" in argv and other_routes:
            output_lines.append("\n🔸 Additional Routes:")
            for route in other_routes:
                output_lines.append(f"  • {route}")

    # ───────────── PORTS ─────────────
    if show_ports:
        output_lines.append(Fore.CYAN + "\n📡 OPEN PORTS (listening):\n")
        try:
            conn_output = subprocess.check_output(["ss", "-tulnp"], stderr=subprocess.DEVNULL).decode()
            lines = conn_output.strip().splitlines()
            if len(lines) <= 1:
                output_lines.append("  [!] No open ports found.")
            else:
                output_lines.append(f"{Style.BRIGHT}{'Proto':<6} {'Local Address':<25} {'PID/Program name'}")
                output_lines.append("-" * 60)
                proto_filter = None
                if "--tcp" in argv:
                    proto_filter = "tcp"
                elif "--udp" in argv:
                    proto_filter = "udp"

                for line in lines[1:]:
                    parts = line.split()
                    proto = parts[0]
                    if proto_filter and proto != proto_filter:
                        continue
                    local = parts[4]
                    pid_prog = parts[-1] if parts[-1] != "-" else "unknown"
                    output_lines.append(f"{proto:<6} {local:<25} {pid_prog}")
        except Exception as e:
            output_lines.append(f"[!] Error retrieving open ports: {e}")

    # ───────────── OUTPUT ─────────────
    final_output = "\n".join(output_lines)
    print(final_output)

    if save_file:
        try:
            with open(save_file, "w", encoding="utf-8") as f:
                f.write(final_output)
            print(Fore.YELLOW + f"\n📁 Output saved to: {save_file}")
        except Exception as e:
            print(Fore.RED + f"[!] Error saving to file: {e}")

