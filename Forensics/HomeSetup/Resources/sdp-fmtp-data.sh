#!/usr/bin/env bash
set -o errexit
set -o nounset
IN_FILE="${1}"
echo "a=fmtp:96 $(tshark -E aggregator=';' -Y sdp.fmtp.parameter -T fields -e sdp.fmtp.parameter -r "${IN_FILE}")"