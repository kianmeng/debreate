# This is a generic Makefile. It will only work on systems with GNU make.

PACKAGE = debreate
VERSION = 0.7.10
prefix = /usr/local
DATAROOT = $(prefix)/share
TARGET = $(DESTDIR)$(DATAROOT)/$(PACKAGE)
BINDIR = $(DESTDIR)$(prefix)/bin
APPSDIR = $(DESTDIR)$(prefix)/share/applications
PIXDIR = $(DESTDIR)$(prefix)/share/pixmaps

INSTALL_DATA = install -vm 0644
INSTALL_EXEC = install -vm 0755
INSTALL_FOLDER = cp -vR
MKDIR = mkdir -vp
UNINSTALL = rm -vf
UNINSTALL_FOLDER = rmdir -v --ignore-fail-on-non-empty

EXEC_SCRIPT = \
\#!/bin/sh \
\n\n$(DATAROOT)/$(PACKAGE)/init.py


FILES = \
	debreate.py \
	common.py \
	db_md5.py \
	db.py \
	language.py \
	panbuild.py \
	panclog.py \
	pancontrol.py \
	pancopyright.py \
	pandepends.py \
	panfiles.py \
	paninfo.py \
	panmenu.py \
	panscripts.py

FILES_EXECUTABLE = \
	init.py

FILES_DB = \
	db/dbabout.py \
	db/dbbuttons.py \
	db/dbcharctrl.py \
	db/dbmessage.py \
	db/dbpathctrl.py \
	db/dbwizard.py

FILES_EXTRA = \
	README

FILES_DOC = \
	docs/changelog \
	docs/gpl-3.0.txt \
	docs/release_notes \
	docs/usage.pdf

BITMAPS = \
	bitmaps/add32.png \
	bitmaps/browse32.png \
	bitmaps/browse64.png \
	bitmaps/build32.png \
	bitmaps/build64.png \
	bitmaps/cancel32.png \
	bitmaps/clear32.png \
	bitmaps/clock16.png \
	bitmaps/confirm32.png \
	bitmaps/debreate64.png \
	bitmaps/del32.png \
	bitmaps/error64.png \
	bitmaps/exit32.png \
	bitmaps/globe16.png \
	bitmaps/import32.png \
	bitmaps/next32.png \
	bitmaps/pipe32.png \
	bitmaps/prev32.png \
	bitmaps/preview32.png \
	bitmaps/preview64.png \
	bitmaps/question64.png \
	bitmaps/save32.png \
	bitmaps/save64.png

MENU = debreate.desktop

DISTPACKAGE = $(PACKAGE)_$(VERSION).tar.xz

DISTDIRS = \
	bitmaps \
	data \
	db \
	docs \
	locale

DISTFILES = \
	$(FILES_EXECUTABLE) \
	$(FILES) \
	$(FILES_EXTRA) \
	Makefile


all:
	@echo "Nothing to be done, run \"make install\""

install: build bin/$(PACKAGE) $(FILES_EXECUTABLE) $(FILES) $(FILES_DB) $(FILES_EXTRA) $(FILES_DOC) $(BITMAPS) locale data/$(MENU)
	@mkdir -vp "$(TARGET)"
	@for py in $(FILES_EXECUTABLE); do \
		$(INSTALL_EXEC) "$${py}" "$(TARGET)"; \
	done
	@for py in $(FILES) $(EXTRA_FILES); do \
		$(INSTALL_DATA) "$${py}" "$(TARGET)"; \
	done
	
	@mkdir -vp "$(TARGET)/db"
	@for py in $(FILES_DB); do \
		$(INSTALL_DATA) "$${py}" "$(TARGET)/db"; \
	done
	
	@$(MKDIR) "$(TARGET)/docs"
	@for doc in $(FILES_DOC); do \
		$(INSTALL_DATA) "$${doc}" "$(TARGET)/docs"; \
	done
	
	@mkdir -vp "$(TARGET)/bitmaps"
	@for png in $(BITMAPS); do \
		$(INSTALL_DATA) "$${png}" "$(TARGET)/bitmaps"; \
	done
	
	@$(INSTALL_FOLDER) locale "$(TARGET)"
	
	@$(MKDIR) "$(BINDIR)"
	@$(INSTALL_EXEC) "bin/$(PACKAGE)" "$(BINDIR)"
	
	@$(MKDIR) "$(PIXDIR)"
	@$(INSTALL_DATA) "bitmaps/debreate64.png" "$(PIXDIR)/debreate.png"
	
	@$(MKDIR) "$(APPSDIR)"
	@$(INSTALL_EXEC) "data/$(MENU)" "$(APPSDIR)"

uninstall:
	@$(UNINSTALL) "$(APPSDIR)/$(MENU)"
	@$(UNINSTALL) "$(PIXDIR)/debreate.png"
	@$(UNINSTALL) "$(BINDIR)/$(PACKAGE)"
	
	@if [ -d "$(TARGET)" ]; then \
		for f in `find "$(TARGET)" -type f`; do \
			$(UNINSTALL) "$${f}"; \
		done; \
		find "$(TARGET)" -type d -empty -delete; \
	fi

build:
	@mkdir -vp "bin"
	@echo "$(EXEC_SCRIPT)\n" > "bin/$(PACKAGE)"

clean:
	@find ./ -type f -name "*.pyc" -print -delete
	@rm -vf "./bin/$(PACKAGE)"
	@if [ -d "./bin" ]; then \
		$(UNINSTALL_FOLDER) "./bin"; \
	fi

distclean: clean

dist:
	@echo "Creating distribution package ..."
	@echo "$(DISTDIRS)"
	@echo "$(DISTFILES)"
	@if [ -f "$(DISTPACKAGE)" ]; then \
		rm -v "$(DISTPACKAGE)"; \
	fi
	@tar -cJf "$(DISTPACKAGE)" $(DISTFILES) $(DISTDIRS)
	@file "$(DISTPACKAGE)"
