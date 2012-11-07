dolibarr-git-hooks
==================

Git hooks for dolibarr development

post-checkout
-------------

### Preresquisite

The script needs an existing conf.php file to run.

### How to use

1. Place this script in the .git/hooks directory

2. Make a symbolic link to post-checkout, i.e. with :
```bash
ln -s post-checkout.py post-checkout
```

3. Checkout a branch and enjoy ^_^

The default behavior uses the branch name stripped of illegal characters as the database name.

#### Configuration (optional)

*See post-checkout.ini.example*

If you want to declare relations manually:

- define branch name / database name relations in a post-checkout.ini file under a [databases] section using statements like :
```branch_name = database_name```

#### Backups

The script generates an timestamped backup of the previous configuration file (just in case).