#!/bin/bash

# Define the aliases to add
ALIASES=("alias python='python3'" "alias pip='pip3'")

# Function to add an alias if it's not already in /etc/profile
add_alias() {
    local alias=$1
    if ! grep -qxF "$alias" /etc/profile; then
        echo "$alias" >> /etc/profile
        echo "Added $alias to /etc/profile"
    else
        echo "$alias already exists in /etc/profile"
    fi
}

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

# Backup /etc/profile
cp /etc/profile /etc/profile.backup

# Add aliases
for alias in "${ALIASES[@]}"; do
    add_alias "$alias"
done

echo "Operation completed."
