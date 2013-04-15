dolibarr-git-hooks
==================

Git hooks for dolibarr development

post-checkout
-------------

### Features

For the moment, this script allows you to manage multiple conf.php files in relation with branches.
This is very usefull to keep your database in sync with the current development or to test different configuration cases.
It simply stores a copy used in a branch and restores it anytime you checkout the said branch.

### How to use

1. Place this script in the .git/hooks directory

2. Checkout a branch and enjoy ^_^
