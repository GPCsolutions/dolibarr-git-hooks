dolibarr-git-hooks
==================

Git hooks for dolibarr development

post-checkout
-------------

### How to use

1. Place this script in the .git/hooks directory

2. Make a symbolic link to post-checkout, i.e. with :
```bash
ln -s post-checkout.py post-checkout
```

3. Define branch name / database name relation in the USER MODIFIABLE PART using statements like :
```python
'branch name': 'database name',
```

4. Checkout a branch and enjoy ^_^

*Note: Make sure you have installed Dolibarr first as the script needs a conf.php file to run*.
