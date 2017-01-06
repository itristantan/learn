#!/bin/bash
# sudo apt-get install autossh
# mimvp.com at 2015-02-09
 
# remote host and port
REMOTE_HOST=mimvp@115.29.237.28
REMOTE_PORT=22
 
# proxy ip addr
IP='91.99.99.11'
 
# proxy port
PORT=1080
 
# proxy spider url
CHECK_URL='http://www.baidu.com'
 
AUTOSSH_MONITOR_PORT=20000
LOG='check_proxy.log'
 
 
function __help(){
    echo 'usage:
    proxy [run | show | check | log]
example:
    proxy run       # run proxy
    proxy show      # show proxy information
    proxy check     # check proxy status
    proxy log       # show proxy log'
}
 
 
function __show(){
    OUTPUT=`ps -ef | grep -v "grep" | grep "autossh"`
    if [[ -n $OUTPUT ]]; then
        echo $OUTPUT
    else
        echo 'Proxy not working'
    fi
}
 
 
# options for autossh:
# -M      specifies the base monitoring port to use.
# -f      run in background (autossh handles this, and does not pass it to ssh.)
#
# options for ssh:
# -q      Quiet mode.
# -T      Disable pseudo-tty allocation.
# -f      Requests ssh to go to background just before command execution.
# -n      Redirects stdin from /dev/null (actually, prevents reading from stdin).  This must be used when ssh is run in the background.
# -N      Do not execute a remote command.  This is useful for just forwarding ports (protocol version 2 only).
# -g      Allows remote hosts to connect to local forwarded ports.
# -D port Specifies a local dynamic application-level port forwarding.
 
function __start(){
    echo 'try to connect remote host...'
    echo "autossh -M $AUTOSSH_MONITOR_PORT -f -qTnNg -D $REMOTE_PORT $REMOTE_HOST"
    autossh -M $AUTOSSH_MONITOR_PORT -f -qTnNg -D $REMOTE_PORT $REMOTE_HOST
    __show
}
 
 
function __check(){
    cmd_4="curl $CHECK_URL -m 10 --socks4 $IP:$PORT"
    cmd_5="curl $CHECK_URL -m 10 --socks5 $IP:$PORT"
    echo "cmd_4 : $cmd_4"
    echo "try to connect proxy $IP:$PORT"
 
    dtime=$(date +'%Y-%m-%d__%H:%M:%S')
    echo $dtime
    RESPONSE=`$cmd_4`
    echo "RESPONSE: $RESPONSE"
    if [[ -n $RESPONSE ]]; then
        echo $RESPONSE
        echo 'Proxy is working...'
        echo "$dtime -- Proxy is working" >> $LOG
    else
        echo 'Proxy not working...'
        echo "$dtime -- Proxy not working" >> $LOG
    fi
}
 
 
if [[ $# -eq 0 ]]; then
    __help
else
    action=$1
    case $action in
        'run')
            __start
            ;;
        'show')
            __show
            ;;
        'check')
            __check
            ;;
        'log')
            tail -n 10 $log
            ;;
        *)
            __help
            ;;
    esac
fi