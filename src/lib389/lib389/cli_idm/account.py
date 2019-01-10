# --- BEGIN COPYRIGHT BLOCK ---
# Copyright (C) 2017, Red Hat inc,
# Copyright (C) 2018, William Brown <william@blackhats.net.au>
# All rights reserved.
#
# License: GPL (version 3 or any later version).
# See LICENSE for details.
# --- END COPYRIGHT BLOCK ---

import argparse

from lib389.idm.account import Account, Accounts
from lib389.cli_base import (
    _generic_list,
    _get_arg,
    )

MANY = Accounts

def list(inst, basedn, log, args):
    _generic_list(inst, basedn, log.getChild('_generic_list'), MANY, args)

def status(inst, basedn, log, args):
    dn = _get_arg( args.dn, msg="Enter dn to check")
    accounts = Accounts(inst, basedn)
    acct = accounts.get(dn=dn)
    acct_str = "locked: %s" % acct.is_locked()
    log.info('dn: %s' % dn)
    log.info(acct_str)

def lock(inst, basedn, log, args):
    dn = _get_arg( args.dn, msg="Enter dn to check")
    accounts = Accounts(inst, basedn)
    acct = accounts.get(dn=dn)
    acct.lock()
    log.info('locked %s' % dn)

def unlock(inst, basedn, log, args):
    dn = _get_arg( args.dn, msg="Enter dn to check")
    accounts = Accounts(inst, basedn)
    acct = accounts.get(dn=dn)
    acct.unlock()
    log.info('unlocked %s' % dn)

def reset_password(inst, basedn, log, args):
    dn = _get_arg(args.dn, msg="Enter dn to reset password")
    new_password = _get_arg(args.new_password, hidden=True, confirm=True,
        msg="Enter new password for %s" % dn)
    accounts = Accounts(inst, basedn)
    acct = accounts.get(dn=dn)
    acct.reset_password(new_password)
    log.info('reset password for %s' % dn)

def change_password(inst, basedn, log, args):
    dn = _get_arg(args.dn, msg="Enter dn to change password")
    cur_password = _get_arg(args.current_password, hidden=True, confirm=False,
        msg="Enter current password for %s" % dn)
    new_password = _get_arg(args.new_password, hidden=True, confirm=True,
        msg="Enter new password for %s" % dn)
    accounts = Accounts(inst, basedn)
    acct = accounts.get(dn=dn)
    acct.change_password(cur_password, new_password)
    log.info('changed password for %s' % dn)


def create_parser(subparsers):
    account_parser = subparsers.add_parser('account', help='Manage generic accounts IE account locking and unlocking.')

    subcommands = account_parser.add_subparsers(help='action')

    list_parser = subcommands.add_parser('list', help='list')
    list_parser.set_defaults(func=list)

    lock_parser = subcommands.add_parser('lock', help='lock')
    lock_parser.set_defaults(func=lock)
    lock_parser.add_argument('dn', nargs='?', help='The dn to lock')

    status_parser = subcommands.add_parser('status', help='status')
    status_parser.set_defaults(func=status)
    status_parser.add_argument('dn', nargs='?', help='The dn to check')

    unlock_parser = subcommands.add_parser('unlock', help='unlock')
    unlock_parser.set_defaults(func=unlock)
    unlock_parser.add_argument('dn', nargs='?', help='The dn to unlock')

    reset_pw_parser = subcommands.add_parser('reset_password', help='Reset the password of an account. This should be performed by a directory admin.')
    reset_pw_parser.set_defaults(func=reset_password)
    reset_pw_parser.add_argument('dn', nargs='?', help='The dn to reset the password for')
    reset_pw_parser.add_argument('new_password', nargs='?', help='The new password to set')

    change_pw_parser = subcommands.add_parser('change_password', help='Change the password of an account. This can be performed by any user (with correct rights)')
    change_pw_parser.set_defaults(func=change_password)
    change_pw_parser.add_argument('dn', nargs='?', help='The dn to change the password for')
    change_pw_parser.add_argument('new_password', nargs='?', help='The new password to set')
    change_pw_parser.add_argument('current_password', nargs='?', help='The accounts current password')


