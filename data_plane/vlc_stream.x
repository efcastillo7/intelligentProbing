spawn "bash"
expect "\\$"

set vlc "cvlc --noaudio --novideo http://10.0.0."
append vlc [lindex $argv 0]
append vlc ":8080"

send "$vlc\r"
sleep 180
send "\003\r"
