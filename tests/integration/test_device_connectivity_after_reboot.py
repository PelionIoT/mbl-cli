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
            cli_cmd = "mbl-cli shell 'su -l -c reboot'"
        reboot_output, exit_status = pexpect.run(cli_cmd, withexitstatus=True)
        assert exit_status == 0

        time.sleep(40)
        for i in range(15):
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
