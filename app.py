import os
import sys

# Ensure DashBoard directory is in sys.path and is current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.join(current_dir, "DashBoard")

if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

os.chdir(dashboard_dir)

# Execute main dashboard entry point
target_app = os.path.join(dashboard_dir, "app.py")
with open(target_app, "r", encoding="utf-8") as f:
    code = f.read()

exec(compile(code, target_app, "exec"), globals())
