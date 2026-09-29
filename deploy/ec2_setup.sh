#!/bin/bash
# ==============================================================================
# TravelGo — EC2 Automated Deployment Script (Amazon Linux 2023 / Ubuntu)
# ==============================================================================
set -e

echo "🚀 Starting TravelGo EC2 Automated Setup..."

# 1. Update and install packages
if command -v dnf &> /dev/null; then
    # Amazon Linux 2023 / RHEL
    sudo dnf update -y
    sudo dnf install -y python3 python3-pip git nginx
elif command -v apt-get &> /dev/null; then
    # Ubuntu / Debian
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip python3-venv git nginx
fi

# 2. Setup Project Directory and Python venv
APP_DIR="/home/ec2-user/TravelGo"
cd "$APP_DIR" || cd "$(pwd)"

echo "📦 Creating virtual environment and installing dependencies..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 3. Setup systemd service
echo "⚙️ Configuring systemd service..."
sudo cp deploy/travelgo.service /etc/systemd/system/travelgo.service
sudo systemctl daemon-reload
sudo systemctl enable travelgo
sudo systemctl restart travelgo

# 4. Configure Nginx
echo "🌐 Configuring Nginx reverse proxy..."
if [ -d "/etc/nginx/conf.d" ]; then
    sudo cp deploy/nginx.conf /etc/nginx/conf.d/travelgo.conf
fi
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "================================================================"
echo "✅ TravelGo Deployment Complete!"
echo "Check service status: sudo systemctl status travelgo"
echo "View application logs: sudo journalctl -u travelgo -f"
echo "================================================================"
