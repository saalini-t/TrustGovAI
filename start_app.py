#!/usr/bin/env python3
"""
TrustGov AI - Development Server Launcher
Run this script to start both backend and frontend servers.
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting TrustGov AI Backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=PROJECT_ROOT
    )
    return backend_process

def start_frontend():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting Frontend Server...")
    frontend_dir = PROJECT_ROOT / "frontend"
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd=frontend_dir
    )
    return frontend_process

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         TRUSTGOV AI - DEV SERVER                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Start backend
        backend = start_backend()
        time.sleep(2)  # Wait for backend to initialize
        
        # Start frontend
        frontend = start_frontend()
        time.sleep(1)
        
        print("""
✅ Servers started successfully!

📡 Backend API:    http://localhost:8000
   API Docs:       http://localhost:8000/docs

🌐 Frontend:       http://localhost:3000

Press Ctrl+C to stop all servers.
        """)
        
        # Open browser
        webbrowser.open("http://localhost:3000")
        
        # Wait for processes
        backend.wait()
        frontend.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        backend.terminate()
        frontend.terminate()
        print("✅ Servers stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
