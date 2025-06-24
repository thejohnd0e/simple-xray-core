# Script for Easy Installation and Configuration of X-ray Core Without GUI

You are likely familiar with control panels like 3x-ui, Marzban, and others. All of these panels are merely graphical front-ends for the X-ray core, designed to simplify its management and configuration. However, the core itself can run perfectly without any panels and can be fully managed via the terminal. The main advantage of using the "bare" core is that you don’t need to bother with domain names and TLS certificates. The core can be installed and administered manually using the official documentation. This script is intended to simplify that process: it automatically installs the core on the server, creates configuration files, and sets up several executable files for easy user management.

## System Requirements

* 1 CPU
* 512 Mb RAM
* 5 Gb disk space
* OS: Tested on Debian 12 x64

## How to Use the Script

To download and run the script, use the following command:

```sh
wget -qO- https://raw.githubusercontent.com/thejohnd0e/simple-xray-core/refs/heads/main/xray-install | bash
```

To uninstall the script, use the following command:

```sh
wget -qO- https://raw.githubusercontent.com/thejohnd0e/simple-xray-core/refs/heads/main/xray-uninstall | bash
```

## User Management Commands

**Show a list of all clients:**

```sh
userlist
```

**Show the connection link and QR code for the main user:**

```sh
mainuser
```

**Create a new user:**

```sh
newuser
```

**Delete a user:**

```sh
rmuser
```

**Generate a connection link for a user:**

```sh
sharelink
```

A file named `help` will be created in the user's home directory with a list of these commands. You can view it using the following command (run from the user's home directory):

```sh
cat help
```

## Useful Links

* [X-ray Core GitHub Repository](https://github.com/XTLS/Xray-core)
* [Official Documentation (Russian)](https://xtls.github.io/ru/)

## Client Apps for Connecting

**Windows**

* [v2rayN](https://github.com/2dust/v2rayN)
* [Furious](https://github.com/LorenEteval/Furious)
* [Invisible Man - Xray](https://github.com/InvisibleManVPN/InvisibleMan-XRayClient)

**Android**

* [v2rayNG](https://github.com/2dust/v2rayNG)
* [X-flutter](https://github.com/XTLS/X-flutter)
* [SaeedDev94/Xray](https://github.com/SaeedDev94/Xray)

**iOS & macOS arm64**

* [Streisand](https://apps.apple.com/app/streisand/id6450534064)
* [Happ](https://apps.apple.com/app/happ-proxy-utility/id6504287215)
* [OneXray](https://github.com/OneXray/OneXray)

**macOS arm64 & x64**

* [V2rayU](https://github.com/yanue/V2rayU)
* [V2RayXS](https://github.com/tzmax/V2RayXS)
* [Furious](https://github.com/LorenEteval/Furious)
* [OneXray](https://github.com/OneXray/OneXray)

**Linux**

* [Nekoray](https://github.com/MatsuriDayo/nekoray)
* [v2rayA](https://github.com/v2rayA/v2rayA)
* [Furious](https://github.com/LorenEteval/Furious)
