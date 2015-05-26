# command line args
set tcp_agent [lindex $argv 0]
set cbr_rate [lindex $argv 1]Mb
set out_file [lindex $argv 2]
set cbr_start [lindex $argv 3]
set cbr_stop [lindex $argv 4]
set tcp_start [lindex $argv 5]
set tcp_stop [lindex $argv 6]
set duration [lindex $argv 7]

# print debug message
# puts "experiment1| tcp_agent: $tcp_agent, cbr_rate: $cbr_rate, \
# out_to: $out_file, cbr_start: $cbr_start, cbr_stop: $cbr_stop, \
# tcp_start: $tcp_start, tcp_stop: $tcp_stop, duration: $duration"

# link defs
set LINK_TYPE duplex-link
set LINK_BANDWIDTH 10Mb
set LINK_DELAY 10ms
set LINK_QUEUE_TYPE DropTail

# CBR defs
set CBR_PACKET_SIZE 1000
set CBR_RANDOM false
set CBR_TYPE CBR

# create a simulator object
set ns [new Simulator]

# trace file
set trace [open $out_file w]
$ns trace-all $trace

# define a 'finish' procedure
proc finish {} {
    global ns trace
    $ns flush-trace
    close $trace
    exit 0
}

# create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

# create links among nodes
$ns $LINK_TYPE $n1 $n2 $LINK_BANDWIDTH $LINK_DELAY $LINK_QUEUE_TYPE
$ns $LINK_TYPE $n2 $n3 $LINK_BANDWIDTH $LINK_DELAY $LINK_QUEUE_TYPE
$ns $LINK_TYPE $n3 $n4 $LINK_BANDWIDTH $LINK_DELAY $LINK_QUEUE_TYPE
$ns $LINK_TYPE $n2 $n5 $LINK_BANDWIDTH $LINK_DELAY $LINK_QUEUE_TYPE
$ns $LINK_TYPE $n3 $n6 $LINK_BANDWIDTH $LINK_DELAY $LINK_QUEUE_TYPE

# set link queue size
$ns queue-limit $n2 $n3 10

# UDP: n2 -> n3
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$udp set fid_ 1
$ns connect $udp $null

# CBR (UDP): n2 -> n3
set cbr [new Application/Traffic/CBR]
$cbr set type_ $CBR_TYPE
$cbr set packet_size_ $CBR_PACKET_SIZE
$cbr set random_ $CBR_RANDOM
$cbr set rate_ $cbr_rate
$cbr attach-agent $udp

# TCP: n1 -> n4
set tcp [new $tcp_agent]
$ns attach-agent $n1 $tcp
set tcp_sink [new Agent/TCPSink]
$ns attach-agent $n4 $tcp_sink
$tcp set fid_ 2
$ns connect $tcp $tcp_sink

# FTP (TCP): n1 -> n4
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

# scheduling
$ns at $cbr_start "$cbr start"
$ns at $tcp_start "$ftp start"
$ns at $tcp_stop "$ftp stop"
$ns at $cbr_stop "$cbr stop"

# call the finish procedure after simulation time
$ns at $duration "finish"

# run script
$ns run
