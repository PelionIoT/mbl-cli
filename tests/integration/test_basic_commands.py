#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import re
import time
import pytest

import pexpect


IPV4_RE = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
DEVICE_HN_RE = r"\d: mbed-linux-os-\d{1,4}: "


@pytest.fixture(scope="module")
def dut_address():
    # Timeout to ensure device is fully booted before running the list cmd.
    time.sleep(60)
    _list = pexpect.run("mbl-cli list")
    print(_list)
    ip_ = _list.decode().strip("\r\n").split("\n")[-1].split(": ")[-1].strip()
    if "fe80" not in ip_:
        raise SystemExit("IP address not found. {} found instead".format(ip_))
    return ip_


class TestSelectCommand:
    def test_select_finds_device_by_ipv6_only(self):
        mbl_cli = pexpect.spawn("mbl-cli", ["select"])
        mbl_cli.expect_exact("Select a device from the list:")
        assert re.search(DEVICE_HN_RE, mbl_cli.before.decode())
        assert not re.search(IPV4_RE, mbl_cli.before.decode())

    def test_select_ctrl_c_behaviour(self):
        mbl_cli = pexpect.spawn("mbl-cli", ["select"])
        mbl_cli.expect_exact("Select a device from the list:")

        mbl_cli.sendcontrol("c")

        mbl_cli.expect_exact("User quit.")
        assert mbl_cli.match

    @pytest.mark.parametrize("bad_input", [b"0", b"a", b"\n", b""])
    def test_select_invalid_input(self, bad_input):
        mbl_cli = pexpect.spawn("mbl-cli", ["select"])
        mbl_cli.expect_exact("Select a device from the list:")

        mbl_cli.sendline(bad_input)

        mbl_cli.expect_exact(
            "Enter a valid device index as shown in the list."
        )
        assert mbl_cli.match


class TestListCommand:
    def test_ipv6_discovered_after_reboot(self, dut_address):
        pexpect.run(
            "mbl-cli -a {} shell 'su -l -c reboot'".format(dut_address)
        )
        # Wait for the device to shut down.
        time.sleep(120)
        # Poll the mbl-cli list for the device.
        # The range(25) is empirical; I've observed 15 attempts is sometimes
        # not enough to allow LAVA to reboot the device fully, and subsequent
        # tests fail.
        for _ in range(25):
            mbl_cli = pexpect.run("mbl-cli list", timeout=60)
            print(mbl_cli.decode())
            ipv4_match = re.search(IPV4_RE, mbl_cli.decode())
            device_match = re.search(
                r"{}".format(dut_address), mbl_cli.decode()
            )
            if device_match is not None:
                break
        assert not ipv4_match
        assert device_match


class TestPutCommand:
    def test_putting_a_file_on_device(self, tmp_path, dut_address):
        tf = tmp_path / "test_file"
        tf.touch(exist_ok=True)
        tf.write_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        output = pexpect.spawn(
            "mbl-cli -a {} put {} /scratch".format(
                dut_address, str(tf.resolve())
            )
        )
        output.expect(pexpect.EOF)
        output.close()
        assert output.exitstatus == 0

    def test_putting_a_dir_on_device(self, tmp_path, dut_address):
        t = tmp_path / "tst"
        t.mkdir(exist_ok=True)
        mbl_cli = pexpect.spawn(
            "mbl-cli -a {} put -r {} /scratch".format(
                dut_address, str(t.resolve())
            )
        )
        mbl_cli.expect(pexpect.EOF)
        mbl_cli.close()
        assert mbl_cli.exitstatus == 0


class TestGetCommand:
    def test_getting_a_file_from_device(self, dut_address):
        output = pexpect.spawn(
            "mbl-cli -a {} get /var/log/mbl-cloud-client.log .".format(
                dut_address
            )
        )
        output.expect(pexpect.EOF)
        output.close()
        assert output.exitstatus == 0

    def test_getting_a_dir_from_device(self, dut_address):
        mbl_cli = pexpect.spawn(
            "mbl-cli -a {} get -r /var/log .".format(dut_address)
        )
        mbl_cli.expect(pexpect.EOF)
        mbl_cli.close()
        assert mbl_cli.exitstatus == 0


class TestShellCommand:
    @pytest.mark.parametrize(
        "cmd, expected",
        [
            ("whoami", "root"),
            ("'for i in $(seq 1 10); do echo $i; sleep 1; done'", "10"),
        ],
    )
    def test_shell_one_shot_cmds(self, cmd, expected, dut_address):
        mbl_cli = pexpect.spawn(
            "mbl-cli -a {} shell {}".format(dut_address, cmd)
        )
        mbl_cli.expect(expected)
        mbl_cli.expect(pexpect.EOF)
        mbl_cli.close()
        assert mbl_cli.exitstatus == 0

    @pytest.mark.parametrize(
        "cmd, expected_code",
        [
            (r"for i in $(seq 1 10); do echo 1; done", 2),
            (r"'rm /scratch'", 1),
            (r"'find uuuuuuuuuuuu'", 1),
        ],
    )
    def test_shell_err_code(self, cmd, expected_code, dut_address):
        mbl_cli = pexpect.spawn(
            "mbl-cli -a {} shell {}".format(dut_address, cmd)
        )
        mbl_cli.expect(pexpect.EOF)
        mbl_cli.close()
        assert mbl_cli.exitstatus == expected_code

    def test_shell_reconnects_after_device_reboot(self, dut_address):
        pexpect.run(
            "mbl-cli -a {} shell 'su -l -c reboot'".format(dut_address)
        )
        time.sleep(90)
        mbl_cli = pexpect.spawn("mbl-cli -a {} shell".format(dut_address))
        mbl_cli.expect(r"root@mbed-linux-os-\d{1,4}:~#")
        mbl_cli.sendline("exit")
        mbl_cli.expect(pexpect.EOF)
        mbl_cli.close()
        assert mbl_cli.exitstatus == 0
