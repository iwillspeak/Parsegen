LOCAL_INCLUDE := $(INCLUDE) -I$(CURRENT_DIR)/include
LOCAL_LIBS    := $(LEX_LIBS)

SRCDIR	:= $(CURRENT_DIR)/src
#TSTDIR  := $(CURRENT_DIR)/tst
OBJDIR	:= $(MAKE_DIR)/build/$(CURRENT_DIR)
#TOBJDIR := $(CURRENT_DIR)/build/debug
PRODDIR := $(MAKE_DIR)/bin

BIN     := $(PRODDIR)/$(CURRENT_TARGET)
#TBIN    := $(PRODDIR)/test

FLXFILES  := $(wildcard $(SRCDIR)/*.l)
CFILES    := $(wildcard $(SRCDIR)/*.c)
#TFILES    := $(wildcard $(TSTDIR)/*.c)
OBJFILES  := $(sort $(CFILES:$(SRCDIR)/%.c=$(OBJDIR)/%.o) $(FLXFILES:$(SRCDIR)/%.l=$(OBJDIR)/%.o))
#TOBJFILES := $(sort $(CFILES:$(SRCDIR)/%.c=$(TOBJDIR)/%.o) $(FLXFILES:$(SRCDIR)/%.l=$(TOBJDIR)/%.o) $(TFILES:$(TSTDIR)/%.c=$(TOBJDIR)/%_tst.o))

$(eval $(call make-exe))

#$(eval $(call test-target))

$(eval $(call clean-target, $(OBJFILES) $(BIN)))