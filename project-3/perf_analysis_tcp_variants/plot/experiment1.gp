# global settings for experiment1
set terminal epslatex color colortext solid
set termoption enhanced
set grid

# settings for plotting experiment1 throughput
set output "../paper/plots/exp1-thp.fig"
set title "Experiment 1 - Throughput"
set xlabel "CBR (Mbps)"
set xrange [6:]
set ylabel "Throughput (MB)"
plot "../out/experiment1/THP-Tahoe.dat" smooth csplines with lines title "Tahoe", \
     "../out/experiment1/THP-Reno.dat" smooth csplines with lines title "Reno", \
     "../out/experiment1/THP-NewReno.dat" smooth csplines with lines title "NewReno", \
     "../out/experiment1/THP-Vegas.dat" smooth csplines with lines title "Vegas"
unset output

# settings for plotting experiment1 drop rate
set output "../paper/plots/exp1-dr.fig"
set title "Experiment 1 - Packets Drop Rate"
set xlabel "CBR (Mbps)"
set xrange [7.5:]
set ylabel "Packets Drop Rate (Percentage)"
plot "../out/experiment1/DR-Tahoe.dat" using 1:($2*100) smooth csplines with lines title "Tahoe", \
     "../out/experiment1/DR-Reno.dat" using 1:($2*100) smooth csplines with lines title "Reno", \
     "../out/experiment1/DR-NewReno.dat" using 1:($2*100) smooth csplines with lines title "NewReno", \
     "../out/experiment1/DR-Vegas.dat" using 1:($2*100) smooth csplines with lines title "Vegas"
unset output

# settings for plotting experiment1 latency
set output "../paper/plots/exp1-lt.fig"
set title "Experiment 1 - Latency"
set xlabel "CBR (Mbps)"
set xrange [8.5:]
set ylabel "Average Latency (ms)"
plot "../out/experiment1/LT-Tahoe.dat" smooth csplines with lines title "Tahoe", \
     "../out/experiment1/LT-Reno.dat" smooth csplines with lines title "Reno", \
     "../out/experiment1/LT-NewReno.dat" smooth csplines with lines title "NewReno", \
     "../out/experiment1/LT-Vegas.dat" smooth csplines with lines title "Vegas"
unset output
