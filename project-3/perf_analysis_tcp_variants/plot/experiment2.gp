# global settings for experiment1
set terminal epslatex color colortext solid
set termoption enhanced
set grid

# settings for plotting experiment2 throughput
set output "../paper/plots/exp2-thp-Reno-Reno.fig"
set title "Experiment 2 - Throughput: Reno/Reno"
set xlabel "CBR (Mbps)"
set xrange [1:10]
set ylabel "Throughput (MB)"
plot "../out/experiment2/THP-Reno_Reno.dat" using 1:2 smooth csplines with lines title "Reno-1", \
     "../out/experiment2/THP-Reno_Reno.dat" using 1:3 smooth csplines with lines title "Reno-2"
unset output

# settings for plotting experiment2 throughput
set output "../paper/plots/exp2-thp-NewReno-Reno.fig"
set title "Experiment 2 - Throughput: NewReno/Reno"
set xlabel "CBR (Mbps)"
set xrange [1:10]
set ylabel "Throughput (MB)"
plot "../out/experiment2/THP-NewReno_Reno.dat" using 1:2 smooth csplines with lines title "NewReno", \
     "../out/experiment2/THP-NewReno_Reno.dat" using 1:3 smooth csplines with lines title "Reno"
unset output

# settings for plotting experiment2 throughput
set output "../paper/plots/exp2-thp-Vegas-Vegas.fig"
set title "Experiment 2 - Throughput: Vegas/Vegas"
set xlabel "CBR (Mbps)"
set xrange [1:10]
set ylabel "Throughput (MB)"
plot "../out/experiment2/THP-Vegas_Vegas.dat" using 1:2 smooth csplines with lines title "Vegas-1", \
     "../out/experiment2/THP-Vegas_Vegas.dat" using 1:3 smooth csplines with lines title "Vegas-2"
unset output

# settings for plotting experiment2 throughput
set output "../paper/plots/exp2-thp-NewReno-Vegas.fig"
set title "Experiment 2 - Throughput: NewReno/Vegas"
set xlabel "CBR (Mbps)"
set xrange [1:10]
set ylabel "Throughput (MB)"
plot "../out/experiment2/THP-NewReno_Vegas.dat" using 1:2 smooth csplines with lines title "NewReno", \
     "../out/experiment2/THP-NewReno_Vegas.dat" using 1:3 smooth csplines with lines title "Vegas"
unset output



# settings for plotting experiment2 drop rate
set output "../paper/plots/exp2-dr-Reno-Reno.fig"
set title "Experiment 2 - Packets Drop Rate: Reno/Reno"
set xlabel "CBR (Mbps)"
set xrange [5:]
set ylabel "Packets Drop Rate (Percentage)"
plot "../out/experiment2/DR-Reno_Reno.dat" using 1:($2*100) smooth csplines with lines title "Reno-1", \
     "../out/experiment2/DR-Reno_Reno.dat" using 1:($3*100) smooth csplines with lines title "Reno-2"
unset output

# settings for plotting experiment2 drop rate
set output "../paper/plots/exp2-dr-NewReno-Reno.fig"
set title "Experiment 2 - Packets Drop Rate: NewReno/Reno"
set xlabel "CBR (Mbps)"
set xrange [5:]
set ylabel "Packets Drop Rate (Percentage)"
plot "../out/experiment2/DR-NewReno_Reno.dat" using 1:($2*100) smooth csplines with lines title "NewReno", \
     "../out/experiment2/DR-NewReno_Reno.dat" using 1:($3*100) smooth csplines with lines title "Reno"
unset output

# settings for plotting experiment2 drop rate
set output "../paper/plots/exp2-dr-Vegas-Vegas.fig"
set title "Experiment 2 - Packets Drop Rate: Vegas/Vegas"
set xlabel "CBR (Mbps)"
set xrange [8:]
set ylabel "Packets Drop Rate (Percentage)"
plot "../out/experiment2/DR-Vegas_Vegas.dat" using 1:($2*100) smooth csplines with lines title "Vegas-1", \
     "../out/experiment2/DR-Vegas_Vegas.dat" using 1:($3*100) smooth csplines with lines title "Vegas-2"
unset output

# settings for plotting experiment2 drop rate
set output "../paper/plots/exp2-dr-NewReno-Vegas.fig"
set title "Experiment 2 - Packets Drop Rate: NewReno/Vegas"
set xlabel "CBR (Mbps)"
set xrange [8:]
set ylabel "Packets Drop Rate (Percentage)"
plot "../out/experiment2/DR-NewReno_Vegas.dat" using 1:($2*100) smooth csplines with lines title "NewReno", \
     "../out/experiment2/DR-NewReno_Vegas.dat" using 1:($3*100) smooth csplines with lines title "Vegas"
unset output


# settings for plotting experiment2 latency
set output "../paper/plots/exp2-lt-Reno-Reno.fig"
set title "Experiment 2 - Latency: Reno/Reno"
set xlabel "CBR (Mbps)"
set xrange [4:]
set ylabel "Average Latency (ms)"
plot "../out/experiment2/LT-Reno_Reno.dat" using 1:2 smooth csplines with lines title "Reno-1", \
     "../out/experiment2/LT-Reno_Reno.dat" using 1:3 smooth csplines with lines title "Reno-2"
unset output

# settings for plotting experiment2 latency
set output "../paper/plots/exp2-lt-NewReno-Reno.fig"
set title "Experiment 2 - Latency: NewReno/Reno"
set xlabel "CBR (Mbps)"
set xrange [4:]
set ylabel "Average Latency (ms)"
plot "../out/experiment2/LT-NewReno_Reno.dat" using 1:2 smooth csplines with lines title "NewReno", \
     "../out/experiment2/LT-NewReno_Reno.dat" using 1:3 smooth csplines with lines title "Reno"
unset output

# settings for plotting experiment2 latency
set output "../paper/plots/exp2-lt-Vegas-Vegas.fig"
set title "Experiment 2 - Latency: Vegas/Vegas"
set xlabel "CBR (Mbps)"
set xrange [4:]
set ylabel "Average Latency (ms)"
plot "../out/experiment2/LT-Vegas_Vegas.dat" using 1:2 smooth csplines with lines title "Vegas-1", \
     "../out/experiment2/LT-Vegas_Vegas.dat" using 1:3 smooth csplines with lines title "Vegas-2"
unset output

# settings for plotting experiment2 latency
set output "../paper/plots/exp2-lt-NewReno-Vegas.fig"
set title "Experiment 2 - Latency: NewReno/Vegas"
set xlabel "CBR (Mbps)"
set xrange [4:]
set ylabel "Average Latency (ms)"
plot "../out/experiment2/LT-NewReno_Vegas.dat" using 1:2 smooth csplines with lines title "NewReno", \
     "../out/experiment2/LT-NewReno_Vegas.dat" using 1:3 smooth csplines with lines title "Vegas"
unset output
