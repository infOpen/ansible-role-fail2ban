# fail2ban

[![Build Status](https://travis-ci.org/infOpen/ansible-role-fail2ban.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-fail2ban)

Install fail2ban package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.0.x
- Ansible 2.1.x
- Ansible 2.2.x
- Ansible 2.3.x

### Running tests

#### Using Docker driver

```
$ tox
```

#### Using Vagrant driver

```
$ MOLECULE_DRIVER=vagrant tox
```

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


# Main configuration
#------------------------------------------------------------------------------
fail2ban_main_config_content: "{{ _fail2ban_main_config_content }}"
fail2ban_main_config_file_path: '/etc/fail2ban/fail2ban.conf'


# Jails configuration
#------------------------------------------------------------------------------
fail2ban_local_jails_config_file_path: '/etc/fail2ban/jail.local'

# Jails
fail2ban_jails: "{{ _fail2ban_jails }}"
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

### Jails

Jails configuration are defined in `fail2ban_jails` dict. Keys are section name
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
