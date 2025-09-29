"""
Production Deployment Script for Care Catalyst
Launches all services in production mode
"""

import subprocess
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import signal

def start_service(command, service_name, port):
    """Start a service and handle errors"""
    try:
        print(f"🚀 Starting {service_name} on port {port}...")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # Give service time to start
        
        if process.poll() is None:  # Process is still running
            print(f"✅ {service_name} started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {service_name} failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting {service_name}: {e}")
        return None

def check_dependencies():
    """Check if all required files exist"""
    required_files = [
        "model/prakriti_model_robust.pkl",
        "model/prakriti_encoder.pkl",
        "apis/Stage1.py",
        "apis/Stage2.py",
        "web_interface.py"
    ]
    
    print("🔍 Checking dependencies...")
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All dependencies found!")
    return True

def main():
    """Main deployment function"""
    print("🌿 Care Catalyst - Production Deployment 🧠")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Deployment failed: Missing dependencies")
        sys.exit(1)
    
    processes = []
    
    try:
        # Get Python executable path
        python_exe = sys.executable
        
        # Service configurations
        services = [
            {
                "command": f'"{python_exe}" -m uvicorn apis.Stage1:app --host 0.0.0.0 --port 8001 --workers 2',
                "name": "Prakriti Classification API",
                "port": 8001
            },
            {
                "command": f'"{python_exe}" -m uvicorn apis.Stage2:app --host 0.0.0.0 --port 8002 --workers 2',
                "name": "Risk Assessment API", 
                "port": 8002
            },
            {
                "command": f'"{python_exe}" -m uvicorn web_interface:app --host 0.0.0.0 --port 8000 --workers 2',
                "name": "Web Interface",
                "port": 8000
            }
        ]
        
        # Start all services
        print("\n🚀 Starting all services...")
        for service in services:
            process = start_service(
                service["command"], 
                service["name"], 
                service["port"]
            )
            if process:
                processes.append(process)
            else:
                raise Exception(f"Failed to start {service['name']}")
        
        print("\n" + "=" * 50)
        print("🎉 Care Catalyst deployed successfully!")
        print("=" * 50)
        print("📱 Access your application:")
        print("   🌐 Web Interface: http://localhost:8000")
        print("   🧬 Prakriti API:  http://localhost:8001/docs") 
        print("   🧠 Risk API:      http://localhost:8002/docs")
        print("\n💡 Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Keep services running
        try:
            while True:
                time.sleep(1)
                # Check if all processes are still running
                for i, process in enumerate(processes):
                    if process.poll() is not None:
                        print(f"⚠️  Service {i+1} stopped unexpectedly")
        
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        
    finally:
        # Clean shutdown
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ All services stopped. Goodbye!")

if __name__ == "__main__":
    main()