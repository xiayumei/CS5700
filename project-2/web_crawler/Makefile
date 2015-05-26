SRC_DIR		:=	./src
MAIN		:=	webcrawler.py
TARGET_DIR	:=	.
TARGET_OBJ	:= webcrawler

$(TARGET_DIR)/$(TARGET_OBJ): make-target
	ln -sf $(SRC_DIR)/$(MAIN) $(TARGET_DIR)/$(TARGET_OBJ)

.PHONY: make-target
make-target:
	$(shell mkdir -p $(TARGET_DIR))

.PHONY: test
test: $(TARGET_DIR)/$(TARGET_OBJ)
	@echo "Kicking off the test.sh script, it might take a few seconds to finish"
	@/bin/bash `pwd`/test/test.sh

.PHONY: all
all: clean $(TARGET_DIR)/$(TARGET_OBJ) test

.PHONY: clean
clean:
	rm -rf $(TARGET_DIR)/$(TARGET_OBJ) $(SRC_DIR)/*.pyc

