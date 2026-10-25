from pathlib import Path
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def script(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


class InstallerSecurityTests(unittest.TestCase):
    installers = ("xray-install", "xray-install-latest")

    def test_installers_enable_strict_mode_and_private_umask(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                self.assertIn("set -Eeuo pipefail", text)
                self.assertIn("umask 077", text)

    def test_cleanup_traps_succeed_when_there_is_nothing_to_remove(self):
        for name in (*self.installers, "xray-update"):
            with self.subTest(name=name):
                text = script(name)
                self.assertNotRegex(text, r"cleanup\(\).*?\[\[.*?&& rm")

    def test_installers_run_preflight_before_package_changes(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                apt_offset = text.index("apt update")
                preflight = text[:apt_offset]
                self.assertRegex(preflight, r"EUID.*-eq 0")
                self.assertIn("/etc/os-release", preflight)
                self.assertIn("x86_64", preflight)
                self.assertIn("systemctl", preflight)
                self.assertRegex(preflight, r"(:443|port 443|PORT.*443)")
                self.assertIn("grep -E ':443$'", preflight)

    def test_installers_verify_release_checksum_in_private_temp_directory(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                self.assertIn("mktemp -d", text)
                self.assertIn("trap", text)
                self.assertIn(".dgst", text)
                self.assertIn("sha256sum", text)
                self.assertIn("gsub(/[[:space:]]/", text)
                self.assertNotIn("cd /tmp", text)
                self.assertNotIn("-O xray.zip", text)

    def test_installers_preserve_existing_configuration(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                config_guard = re.search(
                    r"if \[\[ -[ef] \"?\$?\{?CONFIG_FILE.*?fi", text, re.DOTALL
                )
                self.assertIsNotNone(config_guard)
                self.assertRegex(text, r"chmod 700 .*CONFIG_DIR")
                self.assertRegex(text, r"chmod 600 .*KEYFILE.*CONFIG_FILE|chmod 600 .*CONFIG_FILE.*KEYFILE")

    def test_generated_helpers_use_exact_duplicate_matching(self):
        expected = "any(.inbounds[0].settings.clients[]; .email == $e)"
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                self.assertIn(expected, text)
                self.assertNotIn(".email|index($e)", text)

    def test_sharelink_keeps_menu_output_out_of_command_substitution(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                menu = re.search(r"choose_email\(\).*?^}", text, re.MULTILINE | re.DOTALL)
                if menu is None:
                    self.fail("choose_email function not found")
                self.assertRegex(menu.group(), r"printf .*?>&2")

    def test_mutating_helpers_validate_and_roll_back_configuration(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                self.assertGreaterEqual(text.count("xray run -test"), 2)
                self.assertGreaterEqual(text.count("Config restored"), 2)
                self.assertGreaterEqual(text.count("systemctl is-active --quiet xray"), 3)
                self.assertNotIn("tmp=$(mktemp)\n", text)
                self.assertNotIn("mapfile -t emails < <(jq", text)

    def test_installers_restore_an_existing_binary_after_failed_restart(self):
        for name in self.installers:
            with self.subTest(name=name):
                text = script(name)
                self.assertIn("xray.backup", text)
                self.assertIn("Previous Xray binary restored", text)
                self.assertLess(text.index("run -test -config"), text.index("xray.new"))

    def test_generated_helper_scripts_have_valid_bash_syntax(self):
        bash = shutil.which("bash")
        if bash is None:
            self.skipTest("bash is not available")
        pattern = re.compile(
            r"cat > /usr/local/bin/([a-z]+) <<'EOS'\n(.*?)\nEOS",
            re.DOTALL,
        )
        for installer in self.installers:
            helpers = pattern.findall(script(installer))
            self.assertEqual(5, len(helpers))
            for helper_name, helper_source in helpers:
                with self.subTest(installer=installer, helper=helper_name):
                    result = subprocess.run(
                        [bash, "-n"],
                        input=(helper_source + "\n").encode(),
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr.decode())


class UpdateSecurityTests(unittest.TestCase):
    def test_update_checks_root_platform_architecture_and_systemd(self):
        text = script("xray-update")
        self.assertRegex(text, r"EUID.*-eq 0")
        self.assertIn("/etc/os-release", text)
        self.assertIn("x86_64", text)
        self.assertIn("systemctl", text)

    def test_update_requires_an_existing_installation(self):
        text = script("xray-update")
        self.assertIn("Xray is not installed", text)
        self.assertNotIn("Installing $LATEST", text)
        self.assertRegex(text, r"exit 1")
        self.assertLess(
            text.index("[[ -x $XRAY_BIN"),
            text.index('if [[ ${1:-} == "--install-cron"'),
        )

    def test_update_is_locked_verified_atomic_and_rollback_capable(self):
        text = script("xray-update")
        for expected in (
            "set -Eeuo pipefail",
            "umask 077",
            "flock",
            "mktemp -d",
            ".dgst",
            "sha256sum",
            "xray.new",
            "xray.backup",
            "Previous Xray binary restored",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("systemctl stop xray", text)
        self.assertLess(text.index("sha256sum"), text.index("xray.new"))
        self.assertNotIn("/tmp/xray.zip", text)
        self.assertIn("gsub(/[[:space:]]/", text)


class UninstallSafetyTests(unittest.TestCase):
    def test_uninstall_checks_root_platform_architecture_and_systemd(self):
        text = script("xray-uninstall")
        self.assertRegex(text, r"EUID.*-eq 0")
        self.assertIn("/etc/os-release", text)
        self.assertIn("x86_64", text)
        self.assertIn("systemctl", text)

    def test_uninstall_preserves_shared_packages(self):
        text = script("xray-uninstall")
        self.assertNotRegex(text, r"apt (remove|purge|autoremove)")

    def test_uninstall_removes_only_project_cron_and_log(self):
        text = script("xray-uninstall")
        self.assertIn("crontab -l", text)
        self.assertIn("xray-update", text)
        self.assertIn("/var/log/xray-update.log", text)
        self.assertIn('awk -v job="$cron_job"', text)
        self.assertIn("'$0 != job'", text)

    def test_uninstall_removes_project_owned_bbr_configuration(self):
        path = "/etc/sysctl.d/99-simple-xray-bbr.conf"
        self.assertIn(path, script("xray-install"))
        self.assertIn(path, script("xray-install-latest"))
        self.assertIn(path, script("xray-uninstall"))


class LatestVersionDiscoveryTests(unittest.TestCase):
    def test_latest_installer_does_not_truncate_a_pipe_under_pipefail(self):
        self.assertNotIn("| head -n 1", script("xray-install-latest"))


if __name__ == "__main__":
    unittest.main()
