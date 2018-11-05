# fail2ban

[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-fail2ban/master.svg?label=travis_master)](https://travis-ci.org/infOpen/ansible-role-fail2ban)
[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-fail2ban/develop.svg?label=travis_develop)](https://travis-ci.org/infOpen/ansible-role-fail2ban)
[![Updates](https://pyup.io/repos/github/infOpen/ansible-role-fail2ban/shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-fail2ban/)
[![Python 3](https://pyup.io/repos/github/infOpen/ansible-role-fail2ban/python-3-shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-fail2ban/)
[![Ansible Role](https://img.shields.io/ansible/role/12450.svg)](https://galaxy.ansible.com/infOpen/fail2ban/)

Install fail2ban package.

## Requirements

This role requires Ansible 2.5 or higher,
and platform requirements are listed in the metadata file.

> **Note**: On CentOS 7, you must have EPEL installed

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- CentOS 7
- Debian Jessie
- Debian Stretch
- Ubuntu Xenial
- Ubuntu Bionic

and use:
- Ansible 2.5.x
- Ansible 2.6.x
- Ansible 2.7.x

### Running tests

#### Using Docker driver

```
$ tox
```

You can also configure molecule options and molecule command using environment variables:
* `MOLECULE_OPTIONS` Default: "--debug"
* `MOLECULE_COMMAND` Default: "test

## Role Variables

### Default role variables

``` yaml
# Repositories variables
#------------------------------------------------------------------------------
fail2ban_repository_update_cache: True
fail2ban_repository_cache_valid_time: 3600


# Package variables
#------------------------------------------------------------------------------
fail2ban_package_state: 'present'
fail2ban_packages: "{{ _fail2ban_packages }}"


# Service variables
#------------------------------------------------------------------------------
fail2ban_service_enabled: True
fail2ban_service_name: "{{ _fail2ban_service_name }}"
fail2ban_service_state: 'started'


# Paths
#------------------------------------------------------------------------------
_fail2ban_paths:
  files:
    action: {}
    filter: {}
    main_config:
      path: '/etc/fail2ban/fail2ban.conf'
    jail_local:
      path: '/etc/fail2ban/jail.local'
  folders:
    action:
      path: '/etc/fail2ban/action.d'
    filter:
      path: '/etc/fail2ban/filter.d'
    main:
      path: '/etc/fail2ban'
fail2ban_paths: "{{ _fail2ban_paths }}"


# Configuration
#------------------------------------------------------------------------------
fail2ban_actions: {}
fail2ban_filters: {}
fail2ban_jails: "{{ _fail2ban_jails }}"
fail2ban_main_config_content: "{{ _fail2ban_main_config_content }}"
```

### Debian family role variables

``` yaml
# Package variables
#------------------------------------------------------------------------------
_fail2ban_packages :
  - name: 'fail2ban'


# Service variables
#------------------------------------------------------------------------------
_fail2ban_service_name: 'fail2ban'


# Main configuration
#------------------------------------------------------------------------------
_fail2ban_main_config_content:
  - option: 'loglevel'
    value: 3
  - option: 'logtarget'
    value: '/var/log/fail2ban.log'
  - option: 'syslog-target'
    value: '/var/log/fail2ban.log'
  - option: 'syslog-facility'
    value: 1
  - option: 'socket'
    value: '/var/run/fail2ban/fail2ban.sock'
  - option: 'pidfile'
    value: '/var/run/fail2ban/fail2ban.pid'


# Jails configuration
#------------------------------------------------------------------------------
_fail2ban_jails:
  ssh:
    enabled: true
    port: 'ssh'
    filter: 'sshd'
    logpath: '/var/log/auth.log'
    maxretry: 3
    findtime: 600
```

### Debian Jessie specific role variables

``` yaml
_fail2ban_main_config_content:
  - option: 'loglevel'
    value: 3
  - option: 'logtarget'
    value: '/var/log/fail2ban.log'
  - option: 'socket'
    value: '/var/run/fail2ban/fail2ban.sock'
  - option: 'pidfile'
    value: '/var/run/fail2ban/fail2ban.pid'
```

### Ubuntu Xenial specific role variables

``` yaml
# Main configuration
#------------------------------------------------------------------------------
_fail2ban_main_config_content:
  - option: 'loglevel'
    value: 'INFO'
  - option: 'logtarget'
    value: '/var/log/fail2ban.log'
  - option: 'syslogsocket'
    value: 'auto'
  - option: 'socket'
    value: '/var/run/fail2ban/fail2ban.sock'
  - option: 'pidfile'
    value: '/var/run/fail2ban/fail2ban.pid'
  - option: 'dbfile'
    value: '/var/lib/fail2ban/fail2ban.sqlite3'
  - option: 'dbpurgeage'
    value: 86400


# Jails configuration
#------------------------------------------------------------------------------
_fail2ban_jails:
  sshd:
    enabled: true
    port: 'ssh'
    filter: 'sshd'
    logpath: '/var/log/auth.log'
    maxretry: 3
    findtime: 600
```

## How define ...

### Actions

Actions configurations are defined in `fail2ban_actions` dict. Keys are section
name and values are the section content.

All these actions configs are wrote to their own file.

``` yaml
_fail2ban_actions:
  pf:
    Definition:
      actionstart: ''
      actionstop: ''
      actioncheck: ''
      actionban: '/sbin/pfctl -t <tablename> -T add <ip>/32'
      actionunban: '/sbin/pfctl -t <tablename> -T delete <ip>/32'
    Init:
      tablename: 'fail2ban'
```

### Filters

Filters configurations are defined in `fail2ban_filters` dict. Keys are section
name and values are the section content.

All these filters configs are wrote to their own file.

``` yaml
_fail2ban_filters:
  vsftpd:
    INCLUDES:
      before: 'common.conf'
    Definition:
      __pam_re: '\(?%(__pam_auth)s(?:\(\S+\))?\)?:?'
      _daemon: 'vsftpd'
      failregex = |
        ^%(__prefix_line)s%(__pam_re)s\s+authentication failure; logname=\S* uid=\S* euid=\S* tty=(ftp)? ruser=\S* rhost=<HOST>(?:\s+user=.*)?\s*$
        ^ \[pid \d+\] \[.+\] FAIL LOGIN: Client "<HOST>"\s*$
      ignoreregex: ''
```

### Jails

Jails configurations are defined in `fail2ban_jails` dict. Keys are section name
and values are the section content.

All these jails configs are wrote to `jail.local` file.

``` yaml
_fail2ban_jails:
  ssh:
    enabled: true
    port: 'ssh'
    filter: 'sshd'
    logpath: '/var/log/auth.log'
    maxretry: 3
    findtime: 600
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.fail2ban }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
