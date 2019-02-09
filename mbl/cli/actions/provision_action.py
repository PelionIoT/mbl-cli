from mbl.cli.utils import certificates


def execute(args):
    certificates.create_developer_cert("dev_two")
