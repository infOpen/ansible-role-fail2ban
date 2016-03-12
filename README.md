fail2ban
========

[![Build Status](https://travis-ci.org/infOpen/ansible-role-fail2ban.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-fail2ban)

Install fail2ban package.

Requirements
------------

This role requires Ansible 1.8 or higher, and platform requirements are listed
in the metadata file.

Role Variables
--------------

Default role variables

    # Package variables
    #------------------
    fail2ban_package_state   : present

    # Service variables
    #------------------
    fail2ban_service_state   : started
    fail2ban_service_enabled : True

    fail2ban_loglevel       : 3
    fail2ban_logtarget      : /var/log/fail2ban.log
    fail2ban_syslog_target  : /var/log/fail2ban.log
    fail2ban_syslog_facility: 1
    fail2ban_socket         : /var/run/fail2ban/fail2ban.sock
    fail2ban_pidfile        : /var/run/fail2ban/fail2ban.pid

    fail2ban_ignoreips:
     - 127.0.0.1/8

    fail2ban_bantime    : 600
    fail2ban_maxretry   : 3
    fail2ban_findtime   : 600
    fail2ban_backend    : auto
    fail2ban_destemail  : root@localhost
    fail2ban_banaction  : iptables-multiport
    fail2ban_mta        : sendmail
    fail2ban_protocol   : tcp
    fail2ban_chain      : INPUT
    fail2ban_action     : action_

    fail2ban_services:
      - name    : ssh
        enabled : true
        port    : ssh
        filter  : sshd
        logpath : /var/log/auth.log
        maxretry: 3
        findtime: 600

Dependencies
------------

None

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: achaussier.fail2ban }

License
-------

MIT

Author Information
------------------

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
