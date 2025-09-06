
---

# 2️⃣ setup_fiftyone.sh`
(same as I gave earlier, but stripped of inline `cat` for cleaner repo)

```bash
#!/bin/bash
set -euo pipefail

USER=ubuntu
HOME_DIR=/home/$USER
APP_DIR=$HOME_DIR/fiftyone-demo

echo "[*] Updating packages..."
apt-get update -y
apt-get install -y python3-venv python3-pip git build-essential \
  libgl1 libglib2.0-0 ffmpeg

echo "[*] Setting up venv..."
mkdir -p $APP_DIR
chown $USER:$USER $APP_DIR
runuser -l $USER -c "python3 -m venv $APP_DIR/venv"
runuser -l $USER -c "$APP_DIR/venv/bin/pip install --upgrade pip"
runuser -l $USER -c "$APP_DIR/venv/bin/pip install fiftyone pillow numpy"

echo "[*] Copying demo app and service..."
cp run_demo.py $APP_DIR/
chown $USER:$USER $APP_DIR/run_demo.py
chmod +x $APP_DIR/run_demo.py

cp fiftyone-demo.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now fiftyone-demo.service

echo "[*] Setup complete. Use SSH tunnel to access http://localhost:5151"
