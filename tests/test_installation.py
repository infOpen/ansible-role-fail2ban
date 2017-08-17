"""
Role tests
"""

import ConfigParser
import os
import tempfile
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


# Test packages
def test_packages(host):
    """
    Test package install
    """

    assert host.package('fail2ban').is_installed


# Test configuration
@pytest.mark.parametrize('path', [
    '/etc/fail2ban/fail2ban.conf',
    '/etc/fail2ban/jail.conf',
    '/etc/fail2ban/jail.local',
])
def test_config_files_properties(host, path):
    """
    Test configuration file properties
    """

    config_file = host.file(path)
    assert config_file.user == 'root'
    assert config_file.group == 'root'
    assert config_file.mode == 0o644


def test_main_config_file_content(host):
    """
    Test main configuration file content
    """

    expected_values = []

    if host.system_info.codename.lower() == 'xenial':
        expected_values = [
            ('loglevel', 'INFO'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('syslogsocket', 'auto'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('dbfile', '/var/lib/fail2ban/fail2ban.sqlite3'),
            ('dbpurgeage', '86400'),
        ]
    else:
        expected_values = [
            ('loglevel', '3'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('syslog-target', '/var/log/fail2ban.log'),
            ('syslog-facility', '1'),
        ]

    cfg_file = host.file('/etc/fail2ban/fail2ban.conf')

    # Create a temporary file to check configuration content
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(cfg_file.content_string)
    tmp_file.close()

    config = ConfigParser.ConfigParser()
    config.read(tmp_file.name)

    # Remove temporary file
    os.unlink(tmp_file.name)

    assert config.sections() == ['Definition']
    assert config.items('Definition') == expected_values


def test_local_jails_config_file_content(host):
    """
    Test local jails configuration file content
    """

    ssh_jail_section = 'ssh'

    if host.system_info.codename.lower() == 'xenial':
        ssh_jail_section = 'sshd'

    expected_values = [
        ('ignoreip', '127.0.0.1/8'),
        ('bantime', '600'),
        ('maxretry', '3'),
        ('findtime', '600'),
        ('backend', 'auto'),
        ('destemail', 'root@localhost'),
        ('banaction', 'iptables-multiport'),
        ('mta', 'sendmail'),
        ('protocol', 'tcp'),
        ('chain', 'INPUT'),
        ('action_', (
            'iptables-multiport[name={0}, '
            'port="ssh", '
            'protocol="tcp", '
            'chain="INPUT"]').format(ssh_jail_section)),
        ('action_mw', (
            'iptables-multiport[name={0}, '
            'port="ssh", '
            'protocol="tcp", '
            'chain="INPUT"]\nsendmail-whois['
            'name={0}, '
            'dest="root@localhost", '
            'protocol="tcp", '
            'chain="INPUT"]').format(ssh_jail_section)),
        ('action_mwl', (
            'iptables-multiport['
            'name={0}, '
            'port="ssh", '
            'protocol="tcp", '
            'chain="INPUT"]\n'
            'sendmail-whois-lines['
            'name={0}, '
            'dest="root@localhost", '
            'logpath=/var/log/auth.log, '
            'chain="INPUT"]').format(ssh_jail_section)),
        ('action', (
            'iptables-multiport['
            'name={0}, '
            'port="ssh", '
            'protocol="tcp", '
            'chain="INPUT"]').format(ssh_jail_section)),
        ('enabled', 'true'),
        ('port', 'ssh'),
        ('filter', 'sshd'),
        ('logpath', '/var/log/auth.log'),
    ]

    cfg_file = host.file('/etc/fail2ban/jail.local')

    # Create a temporary file to check configuration content
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(cfg_file.content_string)
    tmp_file.close()

    config = ConfigParser.ConfigParser()
    config.read(tmp_file.name)

    # Remove temporary file
    os.unlink(tmp_file.name)

    assert ssh_jail_section in config.sections()
    assert config.items(ssh_jail_section) == expected_values
