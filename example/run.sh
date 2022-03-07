#!/bin/sh

# --------------------------
# RPC service runner script
# --------------------------

# Start service
nameko run --config config.yaml --backdoor 3000 service
