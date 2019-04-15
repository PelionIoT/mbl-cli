import re
import time
import pexpect
import pytest


@pytest.fixture
def _address(request):
    yield request.config.getoption("--address")


class TestListCommand:
    def test_ipv6_discovered_after_reboot(self, _address):
        if _address:
            cli_cmd = "mbl-cli -a {} shell 'su -l -c reboot'".format(_address)
        else:
            _address = pexpect.run(
                "mbl-cli which"
            ).decode().split("(")[1].split(")")[0].strip()
            cli_cmd = "mbl-cli shell 'su -l -c reboot'"
        cli_reboot = pexpect.spawn(cli_cmd, timeout=120)
        cli_reboot.expect(pexpect.EOF)
        cli_reboot.close()
        exit_status = cli_reboot.exitstatus

        assert exit_status is 0 or exit_status is 255

        time.sleep(40)
        for _ in range(15):
            mbl_cli = pexpect.run("mbl-cli list")
            ipv4_match = re.search(
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", mbl_cli.decode()
            )
            ip_match = re.search(
                r"{}".format(_address), mbl_cli.decode()
            )
            if ip_match is not None:
                break

        assert ip_match
        assert not ipv4_match
