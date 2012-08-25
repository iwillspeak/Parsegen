INCLUDE  := -Iinclude
LIBDIR   := lib

MAKE_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

ifeq ($(shell uname), Linux)
CUNIT_LIB := -Wl,-Bstatic -lcunit -Wl,-Bdynamic
LEX       := flex
LEX_LIBS  := -lfl
CC        := gcc
LD        := ld
AR        := ar
CFLAGS    := -std=c99 -Wall -Werror -pedantic -O0 -g3 -D_GNU_SOURCE
LDFLAGS   := 
LDEXFLG   := -lm -lrt -L$(LIBDIR) -Xlinker -rpath=$(abspath $(LIBDIR))
LIBCMD    = $(CC) -shared -Bdynamic -fpic 
LIBEXT    := .so
SLIBEXT   := .a
else
CUNIT_LIB := -lcunit
LEX       := lex
LEX_LIBS  := -ll
CC        := clang
AR        := ar
CFLAGS    := -std=c99 -Wall -Werror -pedantic -O0 -g3
LDFLAGS   := -macosx_version_min 10.5
LDEXFLG   := -L$(LIBDIR)
LIBCMD    = libtool -dynamic -flat_namespace -undefined suppress -install_name $(abspath $(LIB))
LIBEXT    := .dylib
SLIBEXT   := .a
endif

ifeq (CUNIT_INSTALL_DIR, "")
	CUNITDIR = $(abspath ../Cunit-bin)
else
	CUNITDIR = $(CUNIT_INSTALL_DIR)
endif

TFLAGS   := -DLEET_DEBUG
TINCLUDE := -I$(CUNITDIR)/include
THARNESS := tst/build/harness.o
TLIBS    := -L$(CUNITDIR)/lib $(CUNIT_LIB)
LDFLAGS  += -L$(LIBDIR)

ALL_LIBS    :=
ALL_EXES    := 
ALL_CLEAN   :=
ALL_TESTS   := 

define clean-target
ALL_CLEAN += clean_$(CURRENT_TARGET)
.PHONY: clean_$(CURRENT_TARGET)
clean_$(CURRENT_TARGET):
	rm -rf $(1)
endef

define _compile-objects
%.c: %.l
	$(LEX) $(LFLAGS) -o $$@ $$<

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	mkdir -p $(dir $(OBJDIR)/%.o)
	$(CC) $(CFLAGS) $(LOCAL_INCLUDE) -c -o $$@ $$<
endef

define make-dylib
ALL_LIBS += $(CURRENT_TARGET)

.PHONY: $(CURRENT_TARGET)
$(CURRENT_TARGET): $(LIB)

$(LIB): $(OBJFILES)
	$(LIBCMD) $(LDFLAGS) $(LDEXFLG) -o $(LIB) $(LOCAL_LIBS) $(OBJFILES)

$(call _compile-objects)
endef

define make-lib
ALL_LIBS += $(CURRENT_TARGET)

.PHONY: $(CURRENT_TARGET)
$(CURRENT_TARGET): $(LIB)

$(LIB): $(OBJFILES)
	$(AR) -rv $(LIB) $(OBJFILES)

$(call _compile-objects)
endef

define make-exe
ALL_EXES += $(CURRENT_TARGET)

.PHONY: $(CURRENT_TARGET)
$(CURRENT_TARGET): $(BIN)

$(BIN): $(OBJFILES)
	mkdir -p $(dir $(BIN))
	$(CC) $(LDEXFLG) -o $(BIN) $(OBJFILES) $(LOCAL_LIBS)

$(call _compile-objects)

.PHONY: run_$(CURRENT_TARGET)
run_$(CURRENT_TARGET): $(BIN)
	$(BIN)
endef

define test-target
ALL_TESTS += test_$(CURRENT_TARGET)
.PHONY: test_$(CURRENT_TARGET)
test_$(CURRENT_TARGET): $(TBIN)
	$(TBIN)

$(TBIN): $(TOBJFILES) $(THARNESS)
	$(CC) $(LDEXFLG) -o $(TBIN) $(TOBJFILES) $(THARNESS) $(LOCAL_LIBS) $(TLIBS)

$(TOBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) $(TFLAGS) $(LOCAL_INCLUDE) -c -o $$@ $$<

$(TOBJDIR)/%_tst.o: $(TSTDIR)/%.c
	$(CC) $(CFLAGS) $(TFLAGS) $(LOCAL_INCLUDE) $(TINCLUDE) -I$(SRCDIR) -c -o $$@ $$<

endef

.PHONY: all
all: all_targets

.PHONY: test
test: all_tests

.PHONY: rebuild
rebuild: clean all

.PHONY: retest
retest: clean all all_tests

CURRENT_DIR    := pine
CURRENT_TARGET := pine
include $(CURRENT_DIR)/Project.mk

.PHONY: list_projects
list_projects:
	@echo $(ALL_EXES) $(ALL_LIBS) $(ALL_TESTS)

.PHONY: all_tests
all_tests: $(ALL_TESTS)

.PHONY: all_targets
all_targets: $(ALL_EXES) $(ALL_LIBS)

.PHONY: clean
clean: $(ALL_CLEAN)
