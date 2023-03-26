#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o errtrace
set -o pipefail

REPLAY_DST_IP="${1}"
IN_PCAP_FILE="${2}"
OUT_PCAP_FILE="${3:-rtp-for-replay.pcap}"
OUT_SDP_FILE="${4:-sdp}"

REPLAY_SRC_IP=$(ip route get "${REPLAY_DST_IP}" | sed -n -r "s/.* src (\S*).*/\1/p")
REPLAY_SRC_DEV=$(ip route get "${REPLAY_DST_IP}" | sed -n -r "s/.* dev (\S*).*/\1/p")
REPLAY_SRC_MAC=$(ip link show "${REPLAY_SRC_DEV}" | sed -n -r "s/.*\/ether (\S*).*/\1/p")
if [ -z "${REPLAY_SRC_MAC}" ]
then
  echo "Error reading source MAC address. Make sure that the destination IP does not belong to this machine".
fi
ping -q -c 1 -- "${REPLAY_DST_IP}" > /dev/null
ARP_PATH=$(which arp)

if [ -x "${ARP_PATH}" ]
then
  ARP_CMD="${ARP_PATH}"
else
  ARP_CMD="sudo ${ARP_PATH}"
fi
REPLAY_DST_MAC=$(${ARP_CMD} -an -- "${REPLAY_DST_IP}" | sed -n -r "s/.* at (\S*).*/\1/p")

read ORIG_SRC_IP ORIG_SRC_MAC ORIG_DST_IP ORIG_DST_MAC RTP_DST_PORT <<<$(\
    tshark -T fields -e ip.src -e eth.src -e ip.dst -e eth.dst -e tcp.dstport -c 1 -r "${IN_PCAP_FILE}")

tcprewrite \
    --fixcsum \
    --srcipmap=${ORIG_SRC_IP}/32:${REPLAY_SRC_IP}/32 \
    --enet-smac=${REPLAY_SRC_MAC} \
    --dstipmap=${ORIG_DST_IP}/32:${REPLAY_DST_IP}/32 \
    --enet-dmac=${REPLAY_DST_MAC} \
    --infile="${IN_PCAP_FILE}" \
    --outfile="${OUT_PCAP_FILE}"

echo "c=IN IP4 ${REPLAY_SRC_IP}
m=video ${RTP_DST_PORT} RTP/AVP 96
a=rtpmap:96 H264/90000" > "${OUT_SDP_FILE}"

echo "Copy file \"$(readlink -e ${OUT_SDP_FILE})\" to player machine, open it in player, then execute:"
echo "  sudo tcpreplay --intf1=${REPLAY_SRC_DEV} '${OUT_PCAP_FILE}'"