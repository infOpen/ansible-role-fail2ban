"""
Role tests
"""

import ConfigParser
import os
import tempfile
import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


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
    distribution = host.system_info.distribution.lower()
    release = host.system_info.release

    if distribution == 'ubuntu' and release == '16.04':
        expected_values = [
            ('loglevel', 'INFO'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('syslogsocket', 'auto'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('dbfile', '/var/lib/fail2ban/fail2ban.sqlite3'),
            ('dbpurgeage', '86400'),
        ]
    elif distribution == 'centos' and release == '7':
        expected_values = [
            ('loglevel', '3'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('syslogsocket', 'auto'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('dbfile', '/var/lib/fail2ban/fail2ban.sqlite3'),
            ('dbpurgeage', '86400'),
            ('syslog-target', '/var/log/fail2ban.log'),
            ('syslog-facility', '1'),
        ]
    elif distribution == 'ubuntu' and release == '18.04':
        expected_values = [
            ('loglevel', '3'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('syslogsocket', 'auto'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('dbfile', '/var/lib/fail2ban/fail2ban.sqlite3'),
            ('dbpurgeage', '1d'),
            ('syslog-target', '/var/log/fail2ban.log'),
            ('syslog-facility', '1'),
        ]
    elif distribution == 'debian' and release == '9':
        expected_values = [
            ('loglevel', '3'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('syslogsocket', 'auto'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
            ('dbfile', '/var/lib/fail2ban/fail2ban.sqlite3'),
            ('dbpurgeage', '86400'),
            ('syslog-target', '/var/log/fail2ban.log'),
            ('syslog-facility', '1'),
        ]
    else:
        expected_values = [
            ('loglevel', '3'),
            ('logtarget', '/var/log/fail2ban.log'),
            ('socket', '/var/run/fail2ban/fail2ban.sock'),
            ('pidfile', '/var/run/fail2ban/fail2ban.pid'),
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
    distribution = host.system_info.distribution.lower()
    release = host.system_info.release

    if distribution == 'ubuntu' and release == '16.04':
        ssh_jail_section = 'sshd'

    expected_values = [
        ('enabled', 'True'),
        ('filter', 'sshd'),
        ('findtime', '600'),
        ('logpath', '/var/log/auth.log'),
        ('maxretry', '3'),
        ('port', 'ssh'),
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
    assert sorted(config.items(ssh_jail_section)) == expected_values


def test_fake_action_config_file_properties(host):
    """
    Test fake action configuration file properties
    """

    config_file = host.file('/etc/fail2ban/action.d/test_role.conf')

    assert config_file.exists
    assert config_file.is_file
    assert config_file.user == 'root'
    assert config_file.group == 'root'
    assert config_file.mode == 0o644


def test_fake_action_config_file_content(host):
    """
    Test fake action configuration file content
    """

    expected_values = {
        'Definition': [
            ('actionstart', 'foo'),
            ('actionstop', 'bar'),
        ],
        'Init': [
            ('foo', 'bar'),
        ],
    }

    cfg_file = host.file('/etc/fail2ban/action.d/test_role.conf')

    # Create a temporary file to check configuration content
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(cfg_file.content_string)
    tmp_file.close()

    config = ConfigParser.ConfigParser()
    config.read(tmp_file.name)

    # Remove temporary file
    os.unlink(tmp_file.name)

    # Check sections
    assert 'Definition' in config.sections()
    assert 'Init' in config.sections()

    # Check items
    assert sorted(config.items('Definition')) == expected_values['Definition']
    assert config.items('Init') == expected_values['Init']


def test_fake_filter_config_file_properties(host):
    """
    Test fake filter configuration file properties
    """

    config_file = host.file('/etc/fail2ban/filter.d/test_role_2.conf')

    assert config_file.exists
    assert config_file.is_file
    assert config_file.user == 'root'
    assert config_file.group == 'root'
    assert config_file.mode == 0o644


def test_fake_filter_config_file_content(host):
    """
    Test fake action configuration file content
    """

    expected_values = {
        'INCLUDES': [
            ('before', 'common.conf'),
        ],
        'Definition': [
            ('failregex', '^foo.*$'),
            ('ignoreregex', '^bar.*$'),
        ],
    }

    cfg_file = host.file('/etc/fail2ban/filter.d/test_role_2.conf')

    # Create a temporary file to check configuration content
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(cfg_file.content_string)
    tmp_file.close()

    config = ConfigParser.ConfigParser()
    config.read(tmp_file.name)

    # Remove temporary file
    os.unlink(tmp_file.name)

    # Check sections
    assert 'INCLUDES' in config.sections()
    assert 'Definition' in config.sections()

    # Check items
    assert config.items('INCLUDES') == expected_values['INCLUDES']
    assert sorted(config.items('Definition')) == expected_values['Definition']
