#!/usr/bin/env python
# -*- coding: utf-8 *-*

# A post-checkout hook for Dolibarr that automatically
# switches databases when checking out branches
# (C)2012 Raphaël Doursenaud <rdoursenaud@gpcsolutions.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess
import re
import time
import shutil
import configparser

errorcode = 0

# Did we change branch ?
# From git hooks documentation, this is provided by the third argument
if sys.argv[3] == '1':
    # New branch name
    try:
        fqbn = subprocess.check_output(['git', 'symbolic-ref',
'--short', 'HEAD'])
    except:
        print("Unable to detect new branch name")
        sys.exit()

    # Strip newline and convert to string
    fqbn = fqbn.rstrip().decode('utf-8')

    # Default is database name = branch name
    newdb = fqbn

    # Is there a configuration file ?
    configpath = os.path.dirname(os.path.realpath(__file__))
    configfile = os.path.join(configpath, 'post-checkout.ini')
    if os.path.exists(configfile):
        config = configparser.ConfigParser()
        config.read(configfile)

        # Search corresponding database name
        if config.has_option('databases', fqbn):
            newdb = config.get('databases', fqbn)

    # Strip illegal mysql database name characters
    newdb = re.sub(r'[^0-9a-zA-Z$_]', '', newdb)

    # Update configuration file
    confpath = os.path.abspath('htdocs/conf')
    conffile = confpath + '/conf.php'
    bakfile = conffile + '.' + time.strftime('%Y%m%d%H%M%S')
    # Let's make a backup
    shutil.copyfile(conffile, bakfile)
    # Let's get the content
    bfh = open(bakfile, 'r')
    content = bfh.read()
    bfh.close()
    # Detect and replace the db_name line
    cfh = open(conffile, 'w')
    oldline = '^\$dolibarr_main_db_name.*'
    newline = '$dolibarr_main_db_name=\'' + newdb + '\';'
    cfh.write(re.sub(oldline, newline, content, flags=re.MULTILINE))
    cfh.close()

    print('Configured database: ' + newdb)

sys.exit(errorcode)
