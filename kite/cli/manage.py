# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from kite.openstack.common import gettextutils

gettextutils.install('kite')

from oslo.config import cfg

from kite.common import service
from kite.db import migration

CONF = cfg.CONF


def do_db_version():
    """Print database's current migration level."""
    print(migration.version())


def do_db_upgrade():
    return migration.upgrade(CONF.command.revision)


def do_db_downgrade():
    return migration.downgrade(CONF.command.revision)


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('db_version')
    parser.set_defaults(func=do_db_version)

    parser = subparsers.add_parser('db_upgrade')
    parser.set_defaults(func=do_db_upgrade)
    parser.add_argument('--revision', nargs='?')

    parser = subparsers.add_parser('db_downgrade')
    parser.set_defaults(func=do_db_downgrade)
    parser.add_argument('--revision', nargs='?')


command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Available commands',
                                handler=add_command_parsers)


def main():
    CONF.register_cli_opt(command_opt)
    service.prepare_service(sys.argv)

    try:
        CONF.command.func()
    except Exception as e:
        sys.exit("ERROR: %s" % e)
