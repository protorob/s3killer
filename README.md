# s3killer

Python + Boto3 - Script to List, Delete Single and Delete all S3 Buckets

**This script is very brutal in the way it works, be very careful.**

Adding your keys in the script is not safe at all, better use your envyronment variables, I've added them here for practicity as this is something you're probably going to use once in a while.

## How to setup?

1. Create a virtual environment
2. PIP install requirements.txt
3. Add your AWS_ACCESS_KEY_ID in line 23
4. Add your AWS_SECRET_ACCESS_KEY in line 24

## Usage

---

### List buckets

This will list all your buckets

```
python s3killer.py list
```

### Delete one bucket

This allows you to delete a single bucket

```
python s3killer.py delete my-bucket
```

### Delete ALL buckets

Dis will DESTROY all of your S3 buckets.

```
python s3killer.py delete-all
```

And that's it.
Have a good day.
