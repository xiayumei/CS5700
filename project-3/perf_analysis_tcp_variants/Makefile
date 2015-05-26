TEX			:=	pdflatex
TEX_FLAGS	:=	-shell-escape
PAPER_DIR	:=	./paper
PAPER_SRC	:=	paper.tex
PDF			:=	paper.pdf
FIG_SRC		:=	figures.tex
FIG			:=	figures.pdf

PLOT		:=	gnuplot
PLOT_DIR	:=	./plot
PLOT_SRC	:=	experiment1.gp experiment2.gp experiment3.gp

NS2_DIR		:=	./ns2
PROC_DIR	:=	./process
OUT_DIR		:=	./out
BACKUP_PATH	:=	./plot_data.tar.gz

$(PAPER_DIR)/$(PDF): plot $(PAPER_DIR)/$(FIG) $(PAPER_DIR)/$(PAPER_SRC)
	@cd $(PAPER_DIR); $(TEX) $(TEX_FLAGS) $(PAPER_SRC)

$(PAPER_DIR)/$(FIG): $(PAPER_DIR)/$(FIG_SRC)
	@cd $(PAPER_DIR); $(TEX) $(TEX_FLAGS) $(FIG_SRC)

.PHONY: plot
plot: $(addprefix $(PLOT_DIR)/, $(PLOT_SRC))
	@mkdir -p $(PAPER_DIR)/plots
	@cd $(PLOT_DIR); $(PLOT) $(PLOT_SRC)

.PHONY: expall
expall: exp1 exp2 exp3

.PHONY: exp1
exp1:
	@cd $(OUT_DIR); find experiment1/ -mindepth 1 -maxdepth 1 -not -name .README -exec rm -rf {} \;
	@cd $(PROC_DIR); ./exec_tcl.py -g 0.01 exp1 -o ../out/experiment1/exp1.tr \
		--cbr-start 0.5 --cbr-stop 49.5 --tcp-start 1.0 --tcp-stop 49.0 \
		--duration 50.0

.PHONY: exp2
exp2:
	@cd $(OUT_DIR); find experiment2/ -mindepth 1 -maxdepth 1 -not -name .README -exec rm -rf {} \;
	@cd $(PROC_DIR); ./exec_tcl.py -g 0.01 exp2 -o ../out/experiment2/exp2.tr \
		--cbr-start 0.5 --cbr-stop 49.5 --tcp1-start 1.0 --tcp1-stop 49.0 \
		--tcp2-start 1.0 --tcp2-stop 49.0 --duration 50.0

.PHONY: exp3
exp3:
	@cd $(OUT_DIR); find experiment3/ -mindepth 1 -maxdepth 1 -not -name .README -exec rm -rf {} \;
	@cd $(PROC_DIR); ./exec_tcl.py exp3 -r 3.0 -o ../out/experiment3/exp3.tr \
		--cbr-start 50.0 --cbr-stop 150.0 --tcp-start 0 --tcp-stop 200.0 \
		--duration 200.0

.PHONY: backup
backup:
	@tar -czf $(BACKUP_PATH) $(OUT_DIR)
	@echo 'Plot data backup to $(BACKUP_PATH)'

.PHONY: usage
usage:
	@cd $(OUT_DIR); du -h

.PHONY: clean
clean:
	cd $(PAPER_DIR); ls | grep -vE "\.tex$$|lib|images" | xargs rm -rf
	cd $(PROC_DIR); rm -rf *.pyc

.PHONY: cleanall
cleanall: clean
	cd $(OUT_DIR); find experiment*/ -mindepth 1 -maxdepth 1 -not -name .README -exec rm -rf {} \;
