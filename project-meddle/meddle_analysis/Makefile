SRC_DIR		:=	./src
OUTPUT_DIR	:=	./output
DATA_DIR	:=	./tcpdump
OUT_SITES	:=	sites_output
OUT_GREP	:=	grep_output


.PHONY: statsip
statsip:
	$(SRC_DIR)/sites_contacted.sh $(DATA_DIR) $(OUTPUT_DIR)/$(OUT_SITES) $(SRC_DIR)

.PHONY: maporgs
maporgs:
	$(SRC_DIR)/ip_to_identity.sh $(OUTPUT_DIR)/$(OUT_SITES)/ipmap.merged.sorted.txt

.PHONY: maporgs-ws
maporgs-ws:
	$(SRC_DIR)/ip_to_identity_with_web_service.sh $(OUTPUT_DIR)/$(OUT_SITES)/ipmap.merged.sorted.txt

.PHONY: mapapps
mapapps:
	python $(SRC_DIR)/identity_to_app.py $(OUTPUT_DIR)/$(OUT_SITES)/orgmap.txt

.PHONY: grepstuff
grepstuff:
	$(SRC_DIR)/grepall.sh $(DATA_DIR) $(OUTPUT_DIR)/$(OUT_GREP) $(SRC_DIR)

.PHONY: clean
clean:
	rm -rf $(OUTPUT_DIR)
