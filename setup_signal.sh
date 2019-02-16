# Download and setup Signal-Cli

SIGNAL_VERSION="0.6.2"
SIGNAL_FNAME="signal-cli-${SIGNAL_VERSION}.tar.gz"
SIGNAL_LINK="https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_VERSION}/${SIGNAL_FNAME}"
SIGNAL_DIR="/opt/signal-cli"

if [[ ! -d "${SIGNAL_DIR}" ]]; then
    echo "Creating ${SIGNAL_DIR}"
    sudo mkdir -p ${SIGNAL_DIR}
else
    echo "${SIGNAL_DIR} already exists"
    echo "Removing old version and creating"
    sudo rm -rI ${SIGNAL_DIR}
    sudo mkdir -p ${SIGNAL_DIR}
fi

# download signal to this directory
if [ ! -d "${SIGNAL_DIR}/bin" ]; then
    echo "Downloading ${SIGNAL_FNAME}"
    wget ${SIGNAL_LINK} -O /tmp/${SIGNAL_FNAME}
    tar -xzvf /tmp/${SIGNAL_FNAME} -C /tmp/
    sudo mv /tmp/signal-cli-${SIGNAL_VERSION}/* ${SIGNAL_DIR}
else
    echo "${SIGNAL_FNAME} already exists"
fi

# setup symlinks to path
if [ ! -f "/usr/local/bin/signal-cli" ]; then
    sudo ln -sf /opt/signal-cli/bin/signal-cli /usr/local/bin
else
    echo "Link already exists"
fi

# sudo apt-get install default-jre
# sudo apt-get install libunixsocket-java

# now setup Signal dbus 
# sudo useradd signal-cli

# copy files to system-d
sudo cp org.asamk.Signal.conf /etc/dbus-1/system.d/
sudo cp org.asamk.Signal.service /usr/share/dbus-1/system-services/
sudo cp signal.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable signal.service
sudo systemctl reload dbus.service

