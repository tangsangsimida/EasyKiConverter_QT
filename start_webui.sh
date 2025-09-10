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
PYTHON_DIR="$SCRIPT_DIR/python"
PYTHON_EXE="$PYTHON_DIR/bin/python3"

# Function to download portable Python
download_portable_python() {
    echo "Downloading portable Python..."
    
    # Create python directory if it doesn't exist
    if [ ! -d "$PYTHON_DIR" ]; then
        mkdir -p "$PYTHON_DIR"
    fi
    
    # Determine OS and architecture
    OS_TYPE="$(uname -s)"
    ARCH_TYPE="$(uname -m)"
    
    echo "Detected OS: $OS_TYPE, Architecture: $ARCH_TYPE"
    
    # Set download URL based on OS and architecture
    if [[ "$OS_TYPE" == "Linux" ]]; then
        if [[ "$ARCH_TYPE" == "x86_64" ]]; then
            # Use a portable Python distribution
            PYTHON_URL="https://github.com/indygreg/python-build-standalone/releases/download/20230507/cpython-3.11.3+20230507-x86_64-unknown-linux-gnu-install_only.tar.gz"
            PYTHON_FILE="python.tar.gz"
        else
            echo "Unsupported architecture: $ARCH_TYPE"
            return 1
        fi
    elif [[ "$OS_TYPE" == "Darwin" ]]; then
        if [[ "$ARCH_TYPE" == "x86_64" ]]; then
            PYTHON_URL="https://github.com/indygreg/python-build-standalone/releases/download/20230507/cpython-3.11.3+20230507-x86_64-apple-darwin-install_only.tar.gz"
            PYTHON_FILE="python.tar.gz"
        elif [[ "$ARCH_TYPE" == "arm64" ]]; then
            PYTHON_URL="https://github.com/indygreg/python-build-standalone/releases/download/20230507/cpython-3.11.3+20230507-aarch64-apple-darwin-install_only.tar.gz"
            PYTHON_FILE="python.tar.gz"
        else
            echo "Unsupported architecture: $ARCH_TYPE"
            return 1
        fi
    else
        echo "Unsupported OS: $OS_TYPE"
        return 1
    fi
    
    # Check if we already have Python downloaded
    if [ -x "$PYTHON_EXE" ]; then
        echo "Found existing portable Python installation"
        return 0
    fi
    
    # Download Python using a domestic mirror if possible
    echo "Downloading Python from $PYTHON_URL..."
    
    # Try to use domestic mirrors first
    MIRROR_URL=""
    if [[ "$OS_TYPE" == "Linux" ]]; then
        # Try Chinese mirrors
        MIRROR_URL="https://ghproxy.com/$PYTHON_URL"
    fi
    
    if [ -n "$MIRROR_URL" ]; then
        echo "Trying domestic mirror: $MIRROR_URL"
        if command -v wget &> /dev/null; then
            wget -O "$SCRIPT_DIR/$PYTHON_FILE" "$MIRROR_URL" || true
        elif command -v curl &> /dev/null; then
            curl -L -o "$SCRIPT_DIR/$PYTHON_FILE" "$MIRROR_URL" || true
        fi
        
        # Check if download was successful
        if [ ! -f "$SCRIPT_DIR/$PYTHON_FILE" ]; then
            echo "Domestic mirror failed, trying original URL..."
            MIRROR_URL=""
        fi
    fi
    
    # If mirror failed or not available, try original URL
    if [ -z "$MIRROR_URL" ] || [ ! -f "$SCRIPT_DIR/$PYTHON_FILE" ]; then
        if command -v wget &> /dev/null; then
            wget -O "$SCRIPT_DIR/$PYTHON_FILE" "$PYTHON_URL"
        elif command -v curl &> /dev/null; then
            curl -L -o "$SCRIPT_DIR/$PYTHON_FILE" "$PYTHON_URL"
        else
            echo "Neither wget nor curl is available. Please install one of them."
            return 1
        fi
    fi
    
    # Extract Python
    echo "Extracting Python..."
    tar -xzf "$SCRIPT_DIR/$PYTHON_FILE" -C "$PYTHON_DIR" --strip-components=1
    
    # Clean up
    rm -f "$SCRIPT_DIR/$PYTHON_FILE"
    
    if [ -x "$PYTHON_EXE" ]; then
        echo "Portable Python installed successfully"
        return 0
    else
        echo "Failed to install portable Python"
        return 1
    fi
}

# Check for Python installation in project directory first
echo "Checking for Python in project directory..."
if [ -x "$PYTHON_EXE" ]; then
    echo "Found Python in project directory"
    PYTHON_CMD="$PYTHON_EXE"
else
    # Check for system Python installation
    echo "Checking system Python environment..."
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "No system Python found. Attempting to download portable Python..."
        if download_portable_python; then
            PYTHON_CMD="$PYTHON_EXE"
        else
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
        fi
    fi
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
# Temporarily disable exit on error for this check
set +e
$PYTHON_CMD -m pip --version > /dev/null 2>&1
PIP_CHECK_RESULT=$?
set -e
if [ $PIP_CHECK_RESULT -ne 0 ]; then
    echo "WARNING: pip is not available."
    echo "Attempting to install pip..."
    
    # For project directory Python, we need to ensure pip is available
    if [[ "$PYTHON_CMD" == "$PYTHON_EXE" ]]; then
        echo "Ensuring pip is available for project Python..."
        $PYTHON_CMD -m ensurepip --upgrade > /dev/null 2>&1 || true
    else
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
    fi
    
    # Verify pip installation
    echo
    echo "Verifying pip installation..."
    # Temporarily disable exit on error for this check
    set +e
    $PYTHON_CMD -m pip --version > /dev/null 2>&1
    PIP_VERIFY_RESULT=$?
    set -e
    if [ $PIP_VERIFY_RESULT -ne 0 ]; then
        echo "ERROR: Failed to install or verify pip."
        echo "Please manually install pip and try again."
        exit 1
    fi
    echo "pip is now available."
else
    echo "pip is available."
fi
echo

# Check if python3-venv module is available (only for system Python)
if [[ "$PYTHON_CMD" != "$PYTHON_EXE" ]]; then
    echo "Checking Python venv module availability..."
    # Test by checking if ensurepip is available (required for venv)
    # Temporarily disable exit on error for this check
    set +e
    $PYTHON_CMD -c "import ensurepip" > /dev/null 2>&1
    VENV_TEST_RESULT=$?
    set -e

    if [ $VENV_TEST_RESULT -ne 0 ]; then
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
        # Test by checking if ensurepip is available (required for venv)
        # Temporarily disable exit on error for this check
        set +e
        $PYTHON_CMD -c "import ensurepip" > /dev/null 2>&1
        VENV_VERIFY_RESULT=$?
        set -e
        
        if [ $VENV_VERIFY_RESULT -ne 0 ]; then
            echo "ERROR: Failed to install or verify python3-venv package."
            echo "Please manually install python3-venv and try again."
            exit 1
        fi
        echo "Python venv module is now available."
    else
        echo "Python venv module is available."
    fi
else
    echo "Using portable Python, venv should be available by default."
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
        echo "Please check your Python installation and try again."
        exit 1
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