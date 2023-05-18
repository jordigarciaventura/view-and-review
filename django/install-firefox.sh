echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
apt-get update
apt-get install -y --no-install-recommends firefox

export PATH=$PATH:./
