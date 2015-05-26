# command line args
set tcp_agent1 [lindex $argv 0]
set tcp_agent2 [lindex $argv 1]
set cbr_rate [lindex $argv 2]Mb
set out_file [lindex $argv 3]
set cbr_start [lindex $argv 4]
set cbr_stop [lindex $argv 5]
set tcp1_start [lindex $argv 6]
set tcp1_stop [lindex $argv 7]
set tcp2_start [lindex $argv 8]
set tcp2_stop [lindex $argv 9]
set duration [lindex $argv 10]

# print debug message
# puts "experiment2| tcp_agent: $tcp_agent1-$tcp_agent2, cbr_rate: $cbr_rate, \
# out_to: $out_file, cbr_start: $cbr_start, cbr_stop: $cbr_stop, \
# tcp1_start: $tcp1_start, tcp1_stop: $tcp1_stop, $tcp2_start: $tcp2_start, \
# tcp2_stop: $tcp2_stop, duration: $duration"

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

# set the queue size on the critical path
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

# TCP1: n1 -> n4
set tcp1 [new $tcp_agent1]
$ns attach-agent $n1 $tcp1
set tcp_sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $tcp_sink1
$tcp1 set fid_ 2
$ns connect $tcp1 $tcp_sink1

# FTP1 (TCP1): n1 -> n4
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

# TCP2: n5 -> n6
set tcp2 [new $tcp_agent2]
$ns attach-agent $n5 $tcp2
set tcp_sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $tcp_sink2
$tcp2 set fid_ 3
$ns connect $tcp2 $tcp_sink2

# FTP2 (TCP2): n5 -> n6
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP

# scheduling
$ns at $cbr_start "$cbr start"
$ns at $tcp1_start "$ftp1 start"
$ns at $tcp2_start "$ftp2 start"
$ns at $tcp1_stop "$ftp1 stop"
$ns at $tcp2_stop "$ftp2 stop"
$ns at $cbr_stop "$cbr stop"

# call the finish procedure after simulation time
$ns at $duration "finish"

# run script
$ns run
