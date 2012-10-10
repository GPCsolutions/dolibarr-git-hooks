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

# How to use:
# Place this script in the .git/hooks directory
# Make a symbolic link to post-checkout
# (ln -s post-checkout.py post-checkout)
# Define branch name / database name relation
# in the USER MODIFIABLE PART using statements like
# 'branch name': 'database name',
# Checkout a branch and enjoy ^_^

databases = {
# -- BEGIN USER MODIFIABLE PART --
'master': 'dolimaster',
'develop': 'dolidev',
# -- END USER MODIFIABLE PART --
}

import sys
import os
import subprocess
import re
import time
import shutil

errorcode = 0

# Did we change branch ?
# From git hooks documentation, this is provided by the third argument
if sys.argv[3] == '1':
    # New branch name
    try:
        fqbn = subprocess.check_output(['git', 'symbolic-ref',
'--short', 'HEAD'])
    except:
        sys.exit()

    # Strip newline and convert to string
    fqbn = fqbn.rstrip().decode('utf-8')

    # Search corresponding db name
    if fqbn in databases:
        newdb = databases[fqbn]

    #  If not found, use branch name
    else:
        print("Warning: Database name unknown for this branch, keeping current database", file=sys.stderr)
        newdb = fqbn
        errorcode = 1
        sys.exit(errorcode)

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
