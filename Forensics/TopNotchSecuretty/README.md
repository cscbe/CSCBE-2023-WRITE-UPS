# TopNotchSecuretty

## Category

Forensic

## Estimated difficulty

Easy

## Description

Git folder, you have to look at past commits to find the flag in the source code

## Scenario

Only top notch securetty researchers know my tactics!

## Write-up

Doing a ls -lah shows a hidden .git repository.
Exploring the commits give the following:

```
┌──(hutchyy㉿hutchyy)-[/TopNotchSecuretty]
└─$ git log --all --full-history
commit 11cfb960a71a7945fcdf4226373513a166b4be16 (HEAD -> master)
Author: Claudy Focan <claudy.focan@photography.be>
Date:   Fri Jan 6 08:10:12 2023 +0100

    improved security by 200%!

commit be390b62f6ea20cfb8f40cce79b7471cccb0515c
Author: Claudy Focan <hutchyy@hutchyy.localdomain>
Date:   Fri Jan 6 08:07:14 2023 +0100

    first commit!
```

We are currently at the second commit, let's move to the first commit!

```
┌──(hutchyy㉿hutchyy)-[/TopNotchSecuretty]
└─$ git checkout be390b62f6ea20cfb8f40cce79b7471cccb0515c
Note: switching to 'be390b62f6ea20cfb8f40cce79b7471cccb0515c'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at be390b6 first commit!
```

Moving to the fist commit, the only file is main.py, let's check what is in there:

```
┌──(hutchyy㉿hutchyy)-[/TopNotchSecuretty]
└─$ cat main.py
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import sqlite3


app = Flask(__name__)
jwt = JWTManager(app)

# Making a Connection with MongoClient
conn = sqlite3.connect('users.db')


# JWT Config
app.config["JWT_SECRET_KEY"] = r"CSC{s3cret_c4n_be_stor3d_here_right???}"

...
```

## PoC script

-

## Flag

CSC{s3cret_c4n_be_stor3d_here_right???}

## Creator

Julian Dotreppe

## Creator bio

-
