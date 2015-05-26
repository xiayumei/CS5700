# global settings for experiment1
set terminal epslatex color colortext solid
set termoption enhanced
set grid

# settings for plotting experiment3 throughput
set output "../paper/plots/exp3-thp.fig"
set title "Experiment 3 - Throughput"
set xlabel "Time (second)"
set xrange [0:200]
set ylabel "Bandwidth (MBps)"
set yrange [0:2]
plot "../out/experiment3/THP-Reno_DropTail.dat" title "Reno DropTail" with lines smooth bezier, \
     "../out/experiment3/THP-Reno_RED.dat" title "Reno RED" with lines smooth bezier, \
     "../out/experiment3/THP-Sack_DropTail.dat" title "Sack DropTail" with lines smooth bezier, \
     "../out/experiment3/THP-Sack_RED.dat" title "Sack RED" with lines smooth bezier
unset output

# settings for plotting experiment3 latency
set output "../paper/plots/exp3-lt.fig"
set title "Experiment 3 - Latency"
set xlabel "Time (second)"
set xrange [0:200]
set ylabel "Latency (ms)"
set yrange [0:1000]
plot "../out/experiment3/LT-Reno_DropTail.dat" title "Reno DropTail" with lines, \
     "../out/experiment3/LT-Reno_RED.dat" title "Reno RED" with lines, \
     "../out/experiment3/LT-Sack_DropTail.dat" title "Sack DropTail" with lines, \
     "../out/experiment3/LT-Sack_RED.dat" title "Sack RED" with lines
unset output
