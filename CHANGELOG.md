# Changelog

## 2026-10-08

### Security

- Added preflight checks for root privileges, Debian/Ubuntu, x86_64 architecture, systemd, Xray version, and port 443.
- Added SHA-256 verification for downloaded Xray archives before extraction.
- Replaced predictable `/tmp/xray.zip` usage with private temporary directories and guaranteed cleanup.
- Added strict Bash error handling and rollback of the previous Xray binary after failed installation or update.
- Made updates lockable, staged, atomic, and automatically recoverable when the service fails to start.
- Prevented `xray-update` from treating a missing installation as a fresh installation.
- Set private permissions for the Xray configuration directory, configuration file, and Reality keys.
- Made repeated installation preserve existing configuration, keys, and users.
- Made user-management changes validate candidate configuration before replacement and restore the previous configuration after a failed restart.
- Prevented helper commands from reporting success after configuration or service errors.
- Fixed exact duplicate-email detection and interactive `sharelink` output handling.
- Updated uninstall to remove project-owned cron, log, and BBR artifacts without removing shared system packages.

### Documentation and Testing

- Added audit regression tests for installer, updater, uninstaller, and generated helper-script behavior.
- Added syntax checks for all entrypoint scripts and generated helper scripts.
- Documented updater limitations, configuration preservation, SHA-256 verification, and rollback behavior in `Readme.md`.
- Documented the `xray-help` file location and purpose in `Readme.md`.
