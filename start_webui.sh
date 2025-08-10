#!/bin/bash

# EasyKiConverter Web UI Launcher for Linux/macOS
# This script automatically sets up the environment and starts the Web UI

set -e  # Exit on any error

echo "====================================="
echo "   EasyKiConverter Web UI Launcher"
echo "====================================="
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_PATH="$SCRIPT_DIR/EasyKiConverter"

# Check for Python installation
echo "Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo
        echo "ERROR: Python is not installed or not found in PATH."
        echo
        echo "Please follow these steps:"
        echo "1. Install Python 3.7+ using your system package manager:"
        echo "   - Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
        echo "   - CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "   - macOS: brew install python3"
        echo "2. Restart your terminal and try again"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Get Python version and check if it meets requirements
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "Python $PYTHON_VERSION detected successfully"

# Check Python version (basic check for 3.x)
if [[ $PYTHON_VERSION =~ ^3\.[7-9]\.|^3\.[1-9][0-9]\. ]]; then
    echo "Python version check passed"
elif [[ $PYTHON_VERSION =~ ^3\. ]]; then
    echo "WARNING: Python $PYTHON_VERSION detected. Recommended version is 3.7+"
    echo "Continuing anyway..."
else
    echo
    echo "ERROR: Python version $PYTHON_VERSION is not supported."
    echo "This project requires Python 3.7 or higher."
    echo "Please upgrade your Python installation."
    echo
    exit 1
fi
echo

# Check if pip is available
echo "Checking pip availability..."
$PYTHON_CMD -m pip --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "WARNING: pip is not available."
    echo "Attempting to install pip..."
    
    # Detect the system and install pip
    if command -v apt &> /dev/null; then
        # Debian/Ubuntu systems
        echo "Detected Debian/Ubuntu system. Installing python3-pip..."
        if command -v sudo &> /dev/null; then
            sudo apt update && sudo apt install -y python3-pip
        else
            apt update && apt install -y python3-pip
        fi
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL systems
        echo "Detected CentOS/RHEL system. Installing python3-pip..."
        if command -v sudo &> /dev/null; then
            sudo yum install -y python3-pip
        else
            yum install -y python3-pip
        fi
    elif command -v dnf &> /dev/null; then
        # Fedora systems
        echo "Detected Fedora system. Installing python3-pip..."
        if command -v sudo &> /dev/null; then
            sudo dnf install -y python3-pip
        else
            dnf install -y python3-pip
        fi
    else
        echo "Could not detect package manager. Please manually install pip:"
        echo "  - Ubuntu/Debian: apt install python3-pip"
        echo "  - CentOS/RHEL: yum install python3-pip"
        echo "  - Fedora: dnf install python3-pip"
        exit 1
    fi
    
    # Verify pip installation
    echo
    echo "Verifying pip installation..."
    $PYTHON_CMD -m pip --version > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install or verify pip."
        echo "Please manually install pip and try again."
        exit 1
    fi
    echo "pip is now available."
else
    echo "pip is available."
fi
echo

# Check if python3-venv module is available
echo "Checking Python venv module availability..."
$PYTHON_CMD -m venv --help > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "WARNING: Python venv module is not available."
    echo "This usually means the python3-venv package is not installed."
    echo
    echo "Attempting to install python3-venv package..."
    
    # Detect the system and install python3-venv
    if command -v apt &> /dev/null; then
        # Debian/Ubuntu systems
        echo "Detected Debian/Ubuntu system. Installing python3-venv..."
        if command -v sudo &> /dev/null; then
            sudo apt update && sudo apt install -y python3-venv
        else
            apt update && apt install -y python3-venv
        fi
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL systems
        echo "Detected CentOS/RHEL system. Installing python3-venv..."
        if command -v sudo &> /dev/null; then
            sudo yum install -y python3-venv
        else
            yum install -y python3-venv
        fi
    elif command -v dnf &> /dev/null; then
        # Fedora systems
        echo "Detected Fedora system. Installing python3-venv..."
        if command -v sudo &> /dev/null; then
            sudo dnf install -y python3-venv
        else
            dnf install -y python3-venv
        fi
    else
        echo "Could not detect package manager. Please manually install python3-venv:"
        echo "  - Ubuntu/Debian: apt install python3-venv"
        echo "  - CentOS/RHEL: yum install python3-venv"
        echo "  - Fedora: dnf install python3-venv"
        exit 1
    fi
    
    # Verify installation
    echo
    echo "Verifying python3-venv installation..."
    $PYTHON_CMD -m venv --help > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install or verify python3-venv package."
        echo "Please manually install python3-venv and try again."
        exit 1
    fi
    echo "Python venv module is now available."
else
    echo "Python venv module is available."
fi
echo

echo "Checking for virtual environment..."

# Check for existing virtual environments
VENV_PATH=""
if [ -d "$SCRIPT_DIR/venv" ]; then
    VENV_PATH="$SCRIPT_DIR/venv"
    echo "Found virtual environment: venv"
elif [ -d "$SCRIPT_DIR/.venv" ]; then
    VENV_PATH="$SCRIPT_DIR/.venv"
    echo "Found virtual environment: .venv"
elif [ -d "$SCRIPT_DIR/env" ]; then
    VENV_PATH="$SCRIPT_DIR/env"
    echo "Found virtual environment: env"
else
    echo "No virtual environment found. Creating new virtual environment..."
    $PYTHON_CMD -m venv "$SCRIPT_DIR/venv"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment."
        echo "This usually means the python3-venv package is not installed."
        echo
        echo "Attempting to install python3-venv package..."
        
        # Detect the system and install python3-venv
        if command -v apt &> /dev/null; then
            # Debian/Ubuntu systems
            echo "Detected Debian/Ubuntu system. Installing python3-venv..."
            if command -v sudo &> /dev/null; then
                sudo apt update && sudo apt install -y python3-venv
            else
                apt update && apt install -y python3-venv
            fi
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL systems
            echo "Detected CentOS/RHEL system. Installing python3-venv..."
            if command -v sudo &> /dev/null; then
                sudo yum install -y python3-venv
            else
                yum install -y python3-venv
            fi
        elif command -v dnf &> /dev/null; then
            # Fedora systems
            echo "Detected Fedora system. Installing python3-venv..."
            if command -v sudo &> /dev/null; then
                sudo dnf install -y python3-venv
            else
                dnf install -y python3-venv
            fi
        else
            echo "Could not detect package manager. Please manually install python3-venv:"
            echo "  - Ubuntu/Debian: apt install python3-venv"
            echo "  - CentOS/RHEL: yum install python3-venv"
            echo "  - Fedora: dnf install python3-venv"
            exit 1
        fi
        
        echo
        echo "Retrying virtual environment creation..."
        $PYTHON_CMD -m venv "$SCRIPT_DIR/venv"
        if [ $? -ne 0 ]; then
            echo "ERROR: Still failed to create virtual environment after installing python3-venv."
            echo "Please check your Python installation and try again."
            exit 1
        fi
    fi
    VENV_PATH="$SCRIPT_DIR/venv"
    echo "Virtual environment created successfully: venv"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment."
    exit 1
fi

echo "Virtual environment activated: $VENV_PATH"
echo

# Set up pip mirror for faster downloads in China
echo "Setting up pip configuration for faster downloads..."
export PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
export PIP_TRUSTED_HOST="pypi.tuna.tsinghua.edu.cn"

# Upgrade pip in virtual environment
echo "Upgrading pip using Tsinghua mirror..."
python -m pip install --upgrade pip -i $PIP_INDEX_URL --trusted-host $PIP_TRUSTED_HOST > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip using mirror, trying default source..."
    python -m pip install --upgrade pip > /dev/null 2>&1
fi

echo "Installing dependencies using domestic mirror for faster speed..."
echo

# Install main requirements if exists
if [ -f "$BASE_PATH/requirements.txt" ]; then
    echo "Installing main project dependencies..."
    pip install -r "$BASE_PATH/requirements.txt" -i $PIP_INDEX_URL --trusted-host $PIP_TRUSTED_HOST
    if [ $? -ne 0 ]; then
        echo "Some main dependencies failed with mirror, trying default source..."
        pip install -r "$BASE_PATH/requirements.txt"
        if [ $? -ne 0 ]; then
            echo "WARNING: Some main dependencies failed to install."
        fi
    fi
    echo "Main dependencies installed successfully!"
else
    echo "WARNING: Main requirements file not found, skipping."
fi

# Install Web UI requirements
echo
echo "Installing Web UI dependencies..."
pip install -r "$BASE_PATH/Web_Ui/requirements.txt" -i $PIP_INDEX_URL --trusted-host $PIP_TRUSTED_HOST
if [ $? -ne 0 ]; then
    echo "Failed with mirror, trying default source..."
    pip install -r "$BASE_PATH/Web_Ui/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Web UI dependencies."
        echo "Please check your internet connection and try again."
        exit 1
    fi
fi
echo "Web UI dependencies installed successfully!"

echo
echo "All dependencies installed successfully!"
echo
echo "====================================="
echo "      Starting Web UI Server"
echo "====================================="
echo
echo "Virtual Environment: $VENV_PATH"
echo "Server URL: http://localhost:8000"
echo
echo "Starting server..."
echo "Your browser will open automatically after startup."
echo "If browser doesn't open, manually navigate to: http://localhost:8000"
echo
echo "Press Ctrl+C to stop the server when you're done."
echo

# Change to the Web UI directory and start the server
cd "$BASE_PATH/Web_Ui"

# Start server and open browser (if available)
if command -v xdg-open &> /dev/null; then
    # Linux
    (sleep 2 && xdg-open http://localhost:8000) &
elif command -v open &> /dev/null; then
    # macOS
    (sleep 2 && open http://localhost:8000) &
fi

# Start the Flask application
python app.py

echo
echo "Server stopped. Deactivating virtual environment..."
deactivate
echo
echo "Virtual environment deactivated."
echo "Thank you for using EasyKiConverter!"
echo