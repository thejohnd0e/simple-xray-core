#!/bin/bash
LATEST=$(curl -s https://api.github.com/repos/XTLS/Xray-core/releases/latest | grep tag_name | cut -d '"' -f4)
CURRENT=$(xray -version | awk '{print $2}')
if [ "$LATEST" != "$CURRENT" ]; then
    systemctl stop xray
    wget https://github.com/XTLS/Xray-core/releases/download/$LATEST/Xray-linux-64.zip -O /tmp/xray.zip
    unzip -o /tmp/xray.zip xray -d /usr/local/bin
    chmod +x /usr/local/bin/xray
    systemctl start xray
    echo "Updated to $LATEST"
fi
