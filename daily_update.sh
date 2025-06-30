#!/bin/bash

# Daily automation script for albert-data-collections
# This script handles: git pull, virtual environment, dependencies and execution

set -e  # Stops the script on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
LOG_FILE="$SCRIPT_DIR/logs/daily_update.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Creating logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Defining logging function
log() {
    echo "[$DATE] $1" | tee -a "$LOG_FILE"
}

log "=== Starting daily update ==="

# Going into the project directory
cd "$SCRIPT_DIR"

# 1. Git pull in order to get the latest version
log "Getting the latest version from the repository..."
if git pull origin main 2>&1 | tee -a "$LOG_FILE"; then
    log "Git pull successful"
else
    log "ERROR: Failed to pull from git repository"
    exit 1
fi

# 2. Creating the virtual environment folder if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log "Creating the virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Activating the virtual environment
log "Activating the virtual environment"
source "$VENV_DIR/bin/activate"

# 4. Install/update dependencies
log "Installing dependencies..."
if pip install -e . 2>&1 | tee -a "$LOG_FILE"; then
    log "Dependencies installed successfully"
else
    log "ERROR: Failed to install dependencies"
    deactivate
    exit 1
fi

# 5. Verifying the existence of the .env file
if [ ! -f ".env" ]; then
    log "WARNING: .env file not found"
fi

# 6. Executing the update script
log "Executing the update script..."
if bash scripts/update_collections_dict.sh 2>&1 | tee -a "$LOG_FILE"; then
    log "Script successfully executed"
else
    log "ERROR: Failed to execute the script"
    deactivate
    exit 1
fi

# 7. Committing changes to the git repository
log "Committing changes to the git repository..."
if git add --all && git commit -m "Daily collections dictionnary update on $(date +'%Y-%m-%d %H:%M:%S')" 2>&1 | tee -a "$LOG_FILE"; then
    log "Changes committed successfully"
else
    log "ERROR: Failed to commit changes to the git repository"
    deactivate
    exit 1
fi

# 8. Pushing changes to the remote repository
log "Pushing changes to the remote repository..."
if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
    log "Changes pushed successfully"
else
    log "ERROR: Failed to push changes to the remote repository"
    deactivate
    exit 1
fi

# 9. Deactivating the virtual environment
deactivate

log "=== Daily update completed ==="
log ""
