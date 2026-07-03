# setup.py
import subprocess
import platform
import os

#def run_command(command):
    #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #output, error = process.communicate()
    #return output.decode(), error.decode()

def run_command(command):
    system = platform.system().lower()
    current_dir = os.getcwd()
    #print(system)
    #print(current_dir)
    if system == 'windows':
        # For Windows, using start cmd.exe /k to open a new command prompt window
        final_command = f'start cmd.exe /k "{command}"'
    elif system == 'darwin':  # macOS
        # Using AppleScript to open a new Terminal window and execute the command
        final_command = f'osascript -e \'tell application "Terminal" to do script "cd {current_dir};{command}"\''
    elif system == 'linux':
        # Linux command (for GNOME)
        final_command = f'gnome-terminal -- bash -c "{command}; exec bash"'
    else:
        print("Unsupported operating system.")
        return "", "Unsupported operating system."

    if system == 'windows':
        # On Windows, subprocess.run can be used directly
        process = subprocess.run(final_command, shell=True)
        return "", ""  # No direct way to capture output/error in a new window
    else:
        # For Linux/macOS, subprocess.Popen is used for compatibility with the terminal command
        process = subprocess.Popen(final_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output.decode(), error.decode()
        
def install_backend_dependencies():
    print("Installing Backend Dependencies...")
    run_command("venv\\Scripts\\activate && python -m pip install -r requirements.txt")
    
def install_backend_dependencies_and_start_backend():
    system = platform.system().lower()
    if system == "windows":
        run_command("python -m venv venv && venv\\Scripts\\activate && python -m pip install -r requirements.txt&& python manage.py migrate && python manage.py load_scaling && python manage.py runserver 8026")
    else:
        # run_command("python3 -m venv venv")
        run_command("python3 -m venv venv && source venv/bin/activate && python3 -m pip install -r requirements.txt && python3 manage.py migrate && python3 manage.py load_scaling && python3 manage.py runserver 8026")

def install_frontend_dependencies():
    print("Installing Frontend Dependencies...")
    os.chdir("frontend/atar_calculator")
    run_command("npm install")
    os.chdir("../..")  # Change back to the root directory

def install_frontend_dependencies_and_start_frontend():
    print("Installing Frontend Dependencies...")
    os.chdir("frontend/atar_calculator")
    run_command("npm install&& npm start")
    os.chdir("../..")  # Change back to the root directory

def setup_virtual_environment():
    print("Setting up Virtual Environment...")
    run_command("python -m venv venv")

def start_backend():
    print("Starting Django Backend...")
    system = platform.system().lower()
    if system == "windows":
        start_backend_command = "venv\\Scripts\\activate && python manage.py migrate && python manage.py load_scaling && python manage.py runserver 8026"
        #start_backend_command = "python manage.py migrate && python manage.py load_scaling && python manage.py runserver 8026"

    elif system == "darwin" or system == "linux":
        start_backend_command = "python manage.py migrate && python manage.py load_scaling && python manage.py runserver 8026"
    else:
        print("Unsupported operating system.")
        return
    # run_command("source venv/bin/activate && python manage.py migrate && python manage.py load_scaling && python manage.py runserver 8026")
    run_command(start_backend_command)
        
def start_frontend():
    print("Starting React Frontend...")
    os.chdir("frontend/atar_calculator")  # Change to the frontend directory
    run_command("npm start")
    os.chdir("../..")  # Change back to the root directory

def main():
    #setup_virtual_environment()
    install_backend_dependencies_and_start_backend()
    install_frontend_dependencies_and_start_frontend()
    #start_backend()
    #start_frontend()
if __name__ == "__main__":
    main()
