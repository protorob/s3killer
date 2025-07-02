#!/usr/bin/env python3
"""
s3killer.py
List, delete one, or delete all S3 buckets.

USAGE
-----
# List buckets
python s3killer.py list

# Delete one bucket
python s3killer.py delete my-bucket

# Delete ALL buckets
python s3killer.py delete-all
"""
import argparse
import sys
import boto3
from botocore.exceptions import ClientError

# ── 1. AWS CREDENTIALS ─────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = "YOUR_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"
# For temporary STS credentials, add a session token (else leave None):
AWS_SESSION_TOKEN     = None
AWS_REGION            = "us-east-1"          # e.g. "eu-west-1", "ap-southeast-2"

# ── 2. SESSION & S3 RESOURCE ───────────────────────────────────────────────────
session = boto3.Session(
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    aws_session_token     = AWS_SESSION_TOKEN,
    region_name           = AWS_REGION,
)
s3 = session.resource("s3")

# ── 3. HELPER FUNCTIONS ────────────────────────────────────────────────────────
def list_buckets() -> None:
    """Print every bucket name in the account."""
    print("Buckets in your account:")
    for bucket in s3.buckets.all():
        print(f"  • {bucket.name}")

def empty_bucket(bucket_name: str) -> None:
    """
    Remove *everything* from a bucket, including all object versions
    and delete markers (so versioned buckets are handled too).
    """
    s3.Bucket(bucket_name).object_versions.delete()

def delete_bucket(bucket_name: str) -> None:
    """Empty then delete a single bucket."""
    try:
        print(f"Emptying bucket '{bucket_name}' …")
        empty_bucket(bucket_name)

        print(f"Deleting bucket '{bucket_name}' …")
        s3.Bucket(bucket_name).delete()
        print("✓ Done.\n")
    except ClientError as err:
        print(f"✗ Could not delete '{bucket_name}': {err}")
        sys.exit(1)

def delete_all_buckets() -> None:
    """Iterate through every bucket, empty and delete it."""
    for bucket in s3.buckets.all():
        delete_bucket(bucket.name)

# ── 4. COMMAND-LINE INTERFACE ──────────────────────────────────────────────────
def get_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="List or delete S3 buckets.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("list",        help="List all buckets")
    d = sub.add_parser("delete",  help="Delete ONE bucket")
    d.add_argument("bucket_name")

    sub.add_parser("delete-all",  help="Delete EVERY bucket (dangerous!)")
    return p

def main() -> None:
    args = get_parser().parse_args()

    if args.command == "list":
        list_buckets()

    elif args.command == "delete":
        delete_bucket(args.bucket_name)

    elif args.command == "delete-all":
        warn = (
            "\n*** DANGER ***\n"
            "This will permanently delete *every* bucket in your account.\n"
            "Type 'yes' to continue: "
        )
        if input(warn).strip().lower() == "yes":
            delete_all_buckets()
        else:
            print("Aborted.")

if __name__ == "__main__":
    main()
