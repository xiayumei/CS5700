CC			:=	gcc
CFLAGS		:=	-Wall -lssl -lcrypto

OBJS		:=	client.o generic.o common.o ssl.o
SRC_DIR		:=	./src

TARGET_DIR	:=	./target
TARGET_OBJS	:=	$(addprefix $(TARGET_DIR)/,$(OBJS))
TARGET_OBJ	:=	executable
FINAL_OBJ	:=	client

.PHONY: build
build: make-target $(TARGET_DIR)/$(TARGET_OBJ)

$(TARGET_DIR)/$(TARGET_OBJ): $(TARGET_OBJS)
	$(CC) $^ $(CFLAGS) -o $@
	ln -sf $(TARGET_DIR)/$(TARGET_OBJ) $(FINAL_OBJ)

$(TARGET_DIR)/client.o: $(SRC_DIR)/client.c
	$(CC) -c $(SRC_DIR)/client.c -o $(TARGET_DIR)/client.o

$(TARGET_DIR)/generic.o: $(SRC_DIR)/generic.c $(SRC_DIR)/generic.h
	$(CC) -c $(SRC_DIR)/generic.c -o $(TARGET_DIR)/generic.o

$(TARGET_DIR)/ssl.o: $(SRC_DIR)/ssl.c $(SRC_DIR)/ssl.h
	$(CC) -c $(SRC_DIR)/ssl.c -o $(TARGET_DIR)/ssl.o

$(TARGET_DIR)/common.o: $(SRC_DIR)/common.c $(SRC_DIR)/common.h
	$(CC) -c $(SRC_DIR)/common.c -o $(TARGET_DIR)/common.o

.PHONY: all
all: clean build test

.PHONY: make-target
make-target:
	$(shell mkdir -p $(TARGET_DIR))

.PHONY: test
test: build
	@echo "Kicking off the test.sh script, it might take a few seconds to finish testing"
	@/bin/bash `pwd`/test/test.sh

.PHONY: clean
clean:
	rm -rf $(FINAL_OBJ) $(TARGET_DIR)

