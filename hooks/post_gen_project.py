from pathlib import Path


# Purpose:
# This hook script is executed after a project is generated
# (e.g., by copying). Some Windows systems write files with CRLF
# ("\r\n") line endings. Shell scripts with CRLF can fail under Unix/Linux
# or in containers. This script recursively converts all
# `*.sh` files in the project directory to LF ("\n") line endings.

# Notes:
# - The script only changes line endings; it does not modify the content otherwise.

# - Typically executed automatically as a post-generation hook.


path: Path
for path in Path(".").glob("**/*.sh"):
    data = path.read_bytes()
    # Replace CRLF (Windows) with LF (Unix) to ensure shell scripts run
    lf_data = data.replace(b"\r\n", b"\n")
    path.write_bytes(lf_data)
