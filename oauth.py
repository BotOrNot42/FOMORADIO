"""
OAuth Module for Fomo
"""
import sys
import argparse
from oauths.twitter import app as twitter_app


# Argument Parser
parser = argparse.ArgumentParser(description="Arguments for the OAuth script")
parser.add_argument("client", type=str, help="Client for OAuth")
args = parser.parse_args()

clients = ["twitter"]

if args.client is None:
    print("Error: You must provide an client")
    print("Supported Clients")
    sys.exit(1)

if args.client == "list":
    print("Supported Clients:")
    for each_client in clients:
        print(f"- {each_client}")
elif args.client == "twitter":
    twitter_app.run()
else:
    print(f"Error: Client can be one of these values <{','.join(clients)}>")
    sys.exit(1)
