signal-send () {
    if [ -z "$1" ]; then
        echo "Usage: signal-send +16215551234 "message" "
    else
        # signal-cli -u +12029305414 send -m "$2" "$1"
        dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.sendMessage string:"$2" array:string: string:"$1"
    fi
}

signal-receive () {
    # signal-cli -u +12029305414 receive
    # signal-cli --dbus-system receive
    # dbus-monitor --system  "interface='org.asamk.Signal'" | grep string
    dbus-monitor --system "interface='org.asamk.Signal'" 
    # while read -r line;
    # do
    #     # ignore the first line
    #     grep -q '.*NameAcquired.*' <<< "$line" && continue
    #     # echo "$line"
    #     grep string <<< "$line" | grep string
    # done
}
