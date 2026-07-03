#!/bin/bash
cd "$(dirname "$0")"

# Check if Homebrew is installed
if command -v brew &> /dev/null
then
    echo "Homebrew is already installed."
else
    # Install Homebrew
    echo "Download & Installing Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install openssl readline sqlite3 xz zlib tcl-tk
    brew install pyenv
fi

# Check if Python is installed
# Install Python using Homebrew

HASPYTHON=`which python3`
if [ ! $HASPYTHON ]; then
    echo "Download & Installing Python"
    brew install python
fi


# # Install Node using Homebrew
# echo "Download & Installing Node"
# brew install node
# Install GLPK using Homebrew

HASGLPK=`brew list | grep glpk`
if [ ! $HASGLPK ]; then 
    echo "Download and Installing GLPK"
    brew install glpk
fi

if [[ ! -d "venv" ]]; then 
    echo "Creating Virtual Environment"
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
else 
    echo "Activate Virtual Environment"
    source venv/bin/activate
    which python3
fi

python3 manage.py runserver 8026

# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# SCRIPT_PATH="$DIR/boot.sh"

# # Make the script executable, just in case
# chmod +x $SCRIPT_PATH

# # AppleScript to open a new Terminal window and run your script
# osascript <<EOF
# tell application "Terminal"
#     do script "sh $SCRIPT_PATH"
# end tell
# EOF
