TRACKERS=$(curl -Ns https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt | awk '$1' | tr '\n' ',')

aria2c \
--allow-overwrite=true \
--bt-enable-lpd=true \
--bt-max-peers=0 \
--bt-tracker="[$TRACKERS]" \
--check-certificate=false \
--daemon=true \
--enable-rpc \
--follow-torrent=mem \
--max-connection-per-server=16 \
--max-overall-upload-limit=1K \
--peer-agent=qBittorrent/4.3.6 \
--peer-id-prefix=-qB4360- \
--seed-time=0 \
--user-agent=qBittorrent/4.3.6
