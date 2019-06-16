## Setting up Signal 

1. Run build_scripts/setup_signal.sh
    
    This will download and install signal to `/opt/signal-cli`, get JRE and setup some files for dbus support
    
    ~~~
    sudo apt-get install default-jre
    sudo apt-get install libunixsocket-java
    ~~~

2. Register a phone number with the `signal-cli` instance

    To link to another device type

    ~~~
    signal-cli link -n NAME
    ~~~
    
    This will provide a link to a QR code you can generate by going to https://zxing.appspot.com/generator and choosing a basic Text QR code.

    To register as a master device

    ~~~
    signal-cli -u +NUMBER register
    ~~~

    Then verify with the SMS code

    ~~~
    signal-cli -u +1NUMBER verify CODE
    ~~~

3. After the script is run `signal-cli` is on the path and you can send messages using the alias

    ~~~
    signal-send +NUMBER "MESSAGE"
    ~~~

    Or can send using dbus directly as

    ~~~
    dbus-send --system --type=method_call --print-reply --dest="org.asamk.Signal" /org/asamk/Signal org.asamk.Signal.sendMessage string:MessageText array:string: string:RECIPIENT
    ~~~

4. There is a python script that also provides some dbus support. You need `pydbus`
    
    ~~~
    pip3 install --user pydbus
    ~~~

## Conda installation

conda install -c conda-forge pygobject
pip install --user pydbus
pip install --user pyzmq
## Documentation

https://github.com/AsamK/signal-cli/wiki/DBus-service
