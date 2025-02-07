# This is a generic Makefile.
# It will only work on systems with GNU make.

# FIXME: "dist" rule compiles gettext locales

# This is written to 'prefix' in 'build' rule, then read in 'install'
prefix=/usr/local
TARGET = $(DESTDIR)$(prefix)

PACKAGE = debreate
VERSION = 0.8
BINDIR = bin
DATAROOT = share
DATADIR = $(DATAROOT)/$(PACKAGE)
APPSDIR = $(DATAROOT)/applications
PIXDIR = $(DATAROOT)/pixmaps
DOCDIR = $(DATADIR)/docs
LOCALEDIR = $(DATAROOT)/locale
ICONTHEME = $(DATAROOT)/icons/gnome
MIMEDIR = $(DATAROOT)/mime/packages
MIMEICONSDIR = $(ICONTHEME)/scalable/mimetypes

PERM_DATA = 0644
PERM_EXEC = 0755

INSTALL_DATA = install -vm ${PERM_DATA}
INSTALL_EXEC = install -vm ${PERM_EXEC}
INSTALL_FOLDER = cp -vR
MKDIR = mkdir -vp
UNINSTALL = rm -vf
LINK = ln -vfs

define MOVE =
	target_dir=$2; \
	source_file=$1; \
	if [ ! -d "$${target_dir}" ]; then \
		$(MKDIR) "$${target_dir}"; \
	fi; \
	mv -vf "$${source_file}" "$${target_dir}"; \
	target_file="$${target_dir}/$$(basename $${source_file})"; \
	chmod -c $(PERM_DATA) "$${target_file}"
endef

UNINSTALL_FOLDER = find "$1" -type f -print -delete; find "$1" -type d -empty -print -delete


FILES_executable = \
	init.py

FILES_root = \
	command_line.py \
	main.py

PACKAGES = \
	dbr \
	f_export \
	fields \
	globals \
	input \
	startup \
	system \
	ui \
	wiz \
	wizbin

PKG_dbr = dbr/*.py
PKG_f_export = f_export/*.py
PKG_fields = fields/*.py
PKG_globals = globals/*.py
PKG_input = input/*.py
PKG_startup = startup/*.py
PKG_system = system/*.py
PKG_ui = ui/*.py
PKG_wiz = wiz/*.py
PKG_wizbin = wizbin/*.py

FILES_extra = \
	README.md \
	INFO

FILES_doc = \
	docs/changelog \
	docs/usage.pdf

FILES_man = \
	man/man1/$(PACKAGE).1

FILES_dist = \
	$(FILES_executable) \
	$(FILES_root) \
	$(FILES_extra) \
	Makefile

DIR_bitmaps = bitmaps
DIR_locale = locale
DIR_templates = templates

FILES_build = \
	$(FILES_executable) \
	$(FILES_root) \
	$(FILES_doc) \
	$(PKG_dbr) \
	$(PKG_f_export) \
	$(PKG_fields) \
	$(PKG_globals) \
	$(PKG_input) \
	$(PKG_startup) \
	$(PKG_system) \
	$(PKG_ui) \
	$(PKG_wiz) \
	$(PKG_wizbin)

DIRS_dist = \
	$(DIR_bitmaps) \
	$(DIR_locale) \
	$(DIR_templates) \
	$(PACKAGES) \
	data \
	debian \
	docs \
	man \
	scripts

PACKAGE_dist = $(PACKAGE)_$(VERSION).tar.xz

FILE_launcher = $(PACKAGE).desktop
FILE_mime = data/mime/$(PACKAGE).xml
FILE_license = docs/LICENSE.txt
FILE_doxyfile = docs/Doxyfile
# INSTALLED = INSTALLED

MIME_prefix = application
MIME_dbp = x-dbp

MIME_icons = \
	data/svg/$(MIME_prefix)-$(MIME_dbp).svg

all:
	@echo "\n\n\tNothing to be done"; \
	echo "\trun one of the following:"; \
	echo "\n\t\t`tput bold`make install`tput sgr0` to install Debreate"; \
	echo "\t\t`tput bold`make help`tput sgr0`    to show a list of options\n"; \

$(INSTALLED)_file:
	@echo "Creating \"$(INSTALLED)\" file ..."; \
	echo "prefix=$(prefix)\n" > "$(INSTALLED)"; \

install:
	@python3 build.py --target install --dir "$(DESTDIR)" --prefix "$(prefix)"

uninstall:
	@python3 build.py --target uninstall --dir "$(DESTDIR)" --prefix "$(prefix)"

install-bitmaps: $(DIR_bitmaps)
	@target="$(DESTDIR)$(prefix)"; \
	data_dir="$${target}/$(DATADIR)"; \
	if [ ! -d "$${data_dir}" ]; then \
		$(MKDIR) "$${data_dir}"; \
	fi; \
	$(INSTALL_FOLDER) "$(DIR_bitmaps)" "$${data_dir}"; \

install-data: $(INSTALLED)
	@target="$(DESTDIR)$(prefix)"; \
	data_dir="$${target}/$(DATADIR)"; \
	if [ ! -d "$${data_dir}" ]; then \
		$(MKDIR) "$${data_dir}"; \
	fi; \
	\
	$(call MOVE,$(INSTALLED),$${data_dir}); \

install-doc: $(FILES_doc) $(FILE_license)
	@target="$(DESTDIR)$(prefix)"; \
	doc_dir="$${target}/$(DOCDIR)"; \
	\
	echo "\nInstalling documentation ..."; \
	$(MKDIR) "$${doc_dir}"; \
	for doc in $(FILES_doc); do \
		$(INSTALL_DATA) "$${doc}" "$${doc_dir}"; \
	done; \
	\
	$(INSTALL_DATA) "$(FILE_license)" "$${doc_dir}"; \

install-icons: $(MIME_icons)
	@target="$(DESTDIR)$(prefix)"; \
	icons_dir="$${target}/$(MIMEICONSDIR)"; \
	$(MKDIR) "$${icons_dir}"; \
	for i in $(MIME_icons); do \
		$(INSTALL_DATA) "$${i}" "$${icons_dir}"; \
	done; \

uninstall-icons:
	@target="$(DESTDIR)$(prefix)"; \
	icons_dir="$${target}/$(ICONTHEME)"; \
	if [ -d "$${icons_dir}" ]; then \
		find "$${icons_dir}" -type f -name "$(MIME_prefix)-$(MIME_dbp)*" -print -delete; \
		find "$${icons_dir}" -type d -empty -print -delete; \
	fi; \

install-launcher: data/$(FILE_launcher)
	@apps_dir=$(TARGET)/$(APPSDIR); \
	$(MKDIR) "$${apps_dir}"; \
	$(INSTALL_DATA) "data/$(FILE_launcher)" "$${apps_dir}"; \

uninstall-launcher:
	@apps_dir=$(TARGET)/$(APPSDIR); \
	$(UNINSTALL) "$${apps_dir}/$(FILE_launcher)"; \

install-locale: $(DIR_locale)
	@target="$(DESTDIR)$(prefix)"; \
	locale_dir="$${target}/$(LOCALEDIR)"; \
	echo "Installing locale files ..."; \
	if [ ! -d "$${locale_dir}" ]; then \
		$(MKDIR) "$${locale_dir}"; \
	fi; \
	for mo in `find $(DIR_locale) -type f -name "*.mo"`; do \
		mo=$$(echo "$${mo}" | sed -e 's:^.......::'); \
		modir="$${locale_dir}/$$(dirname $${mo})"; \
		if [ ! -d "$${modir}" ]; then \
			$(MKDIR) "$${modir}"; \
		fi; \
		$(INSTALL_DATA) "locale/$${mo}" "$${modir}"; \
	done; \

uninstall-locale:
	@target="$(DESTDIR)$(prefix)"; \
	locale_dir="$${target}/$(LOCALEDIR)"; \
	echo "Uninstalling locale files ..."; \
	find "$${locale_dir}" -type f -name "$(PACKAGE)\.mo" -delete; \

install-man: $(FILES_man)
	@target="$(DESTDIR)$(prefix)"; \
	data_root="$${target}/$(DATAROOT)"; \
	for f in $(FILES_man); do \
		filename=$$(basename "$${f}") && mandir="$${data_root}/$$(dirname $${f})"; \
		if [ ! -d "$${mandir}" ]; then \
			$(MKDIR) "$${mandir}"; \
		fi; \
		$(INSTALL_DATA) "$${f}" "$${mandir}"; \
		gzip -vf9 "$${mandir}/$${filename}"; \
	done; \

uninstall-man:
	@target="$(DESTDIR)$(prefix)"; \
	man_dir="$${target}/$(DATAROOT)/man"; \
	if [ -d "$${man_dir}" ]; then \
		echo "Manual dir: $${man_dir}"; \
		find "$${man_dir}/man1" -type f -name "$(PACKAGE)\.1\.gz" -delete; \
	fi; \

install-mime: $(FILE_mime) install-icons
	@target="$(DESTDIR)$(prefix)"; \
	mime_dir="$${target}/$(MIMEDIR)"; \
	if [ ! -d "$${mime_dir}" ]; then \
		$(MKDIR) "$${mime_dir}"; \
	fi; \
	$(INSTALL_DATA) "$(FILE_mime)" "$${mime_dir}"; \

uninstall-mime: uninstall-icons
	@target="$(DESTDIR)$(prefix)"; \
	mime_dir="$${target}/$(MIMEDIR)"; \
	$(UNINSTALL) "$${mime_dir}/$(PACKAGE).xml"; \

install-packages: $(PACKAGES)
	@target="$(DESTDIR)$(prefix)"; \
	data_dir="$${target}/$(DATADIR)"; \
	for pkg in $(PACKAGES); do \
		if [ ! -d "$${data_dir}/$${pkg}" ]; then \
			$(MKDIR) "$${data_dir}/$${pkg}"; \
		fi; \
		pyfiles="$${pkg}/*.py"; \
		for py in $${pyfiles}; do \
			echo "\nInstalling: $${py}"; \
			$(INSTALL_DATA) "$${py}" "$${data_dir}/$${pkg}"; \
		done; \
	done; \

install-templates: $(DIR_templates)
	@target="$(DESTDIR)$(prefix)"; \
	data_dir="$${target}/$(DATADIR)"; \
	if [ ! -d "$${data_dir}" ]; then \
		$(MKDIR) "$${data_dir}"; \
	fi; \
	$(INSTALL_FOLDER) "$(DIR_templates)" "$${data_dir}"; \

doc-html: $(FILE_doxyfile)
	@doxygen "$(FILE_doxyfile)"

doxygen-format: doc-html
	@./scripts/doxygen-format.py

# FIXME: May need to make adjustments
.PHONY: locale
locale:
	@echo "Building gettext locales ..."; \
	locale_dir="$$(pwd)/locale"; \
	for f in $$(find "$${locale_dir}" -type f -name "*.po"); do \
		lc_dir=$$(dirname "$${f}")/LC_MESSAGES; \
		echo "$${lc_dir}"; \
		if [ ! -d "$${lc_dir}" ]; then \
			$(MKDIR) "$${lc_dir}"; \
		fi; \
		msgfmt -v "$${f}" -o "$${lc_dir}/$(PACKAGE).mo"; \
	done; \

dist: distclean deb-clean $(FILES_dist) $(DIRS_dist)
	@echo "Creating distribution package ..."; \
	if [ -f "$(PACKAGE_dist)" ]; then \
		rm -v "$(PACKAGE_dist)"; \
	fi; \
	tar -cJf "$(PACKAGE_dist)" $(FILES_dist) $(DIRS_dist); \
	file "$(PACKAGE_dist)"; \

debianize: dist
	@dh_make -y -n -c mit -e antumdeluge@gmail.com -f "$(PACKAGE_dist)" -p "$(PACKAGE)_$(VERSION)" -i

deb-bin: deb-clean
	@debuild -b -uc -us

deb-bin-signed: deb-clean
	@debuild -b -sa

deb-src: deb-clean
	@debuild -S -uc -us

deb-src-signed: deb-clean
	@debuild -S -sa

clean: doc-clean locale-clean
	@find ./ -type f -name "*.pyc" -print -delete; \
	rm -vf "./bin/$(PACKAGE)"; \
	if [ -d "./bin" ]; then \
		$(call UNINSTALL_FOLDER,./bin); \
	fi; \
	rm -vf "$(INSTALLED)"; \

distclean: clean deb-clean
	@echo "Cleaning distribution ..."; \
	rm -vf "$(PACKAGE_dist)"; \

doc-clean:
	@rm -vrf docs/doxygen

locale-clean:
	@find locale -type f -name "*\.mo" -delete; \
	find locale -type d -empty -delete; \

deb-clean:
	@rm -vrf "debian/$(PACKAGE)" "debian/.debhelper"
	@DEBUILD_FILES="\
	debian/debhelper-build-stamp debian/$(PACKAGE).debhelper.log \
	debian/$(PACKAGE).substvars debian/files"; \
	rm -vf $${DEBUILD_FILES}; \

help:
	@echo "Usage:"; \
	\
	echo "\tmake [command]\n"; \
	\
	echo "Commands:"; \
	\
	echo "\thelp"; \
	echo "\t\t- Show this help dialog\n"; \
	\
	echo "\tall"; \
	echo "\t\t- Does nothing (same as invoking `tput bold`make`tput sgr0` with no"; \
	echo "\t\t  arguments)\n"; \
	\
	echo "\tinstall"; \
	echo "\t\t- Install `tput bold`$(PACKAGE)`tput sgr0` executable & data files onto"; \
	echo "\t\t  the system"; \
	echo "\t\t- Calls `tput bold`install-data`tput sgr0`, `tput bold`install-doc`tput sgr0`, `tput bold`install-launcher`tput sgr0`,"; \
	echo "\t\t  `tput bold`install-locale`tput sgr0`, `tput bold`install-man`tput sgr0`, & `tput bold`install-mime`tput sgr0`\n"; \
	\
	echo "\tuninstall"; \
	echo "\t\t- Remove all installed Debreate files from"; \
	echo "\t\t  the system"; \
	echo "\t\t- Calls `tput bold`uninstall-launcher`tput sgr0`, `tput bold`uninstall-locale`tput sgr0`,"; \
	echo "\t\t  `tput bold`uninstall-man`tput sgr0`, & `tput bold`uninstall-mime`tput sgr0`\n"; \
	\
	echo "\tinstall-bitmaps"; \
	echo "\t\t- Install bitmaps used by application\n"; \
	\
	echo "\tinstall-data"; \
	echo "\t\t- Install misc. data files onto the system\n"; \
	\
	echo "\tinstall-doc"; \
	echo "\t\t- Install documentation files\n"; \
	\
	echo "\tinstall-icons"; \
	echo "\t\t- Install icons for Debreate projects MimeType"; \
	echo "\t\t  registration\n"; \
	\
	echo "\tuninstall-icons"; \
	echo "\t\t- Uninstall Debreate MimeType icons\n"; \
	\
	echo "\tinstall-launcher"; \
	echo "\t\t- Install system menu launcher\n"; \
	\
	echo "\tuninstall-launcher"; \
	echo "\t\t- Uninstall system menu launcher\n"; \
	\
	echo "\tinstall-locale"; \
	echo "\t\t- Install gettext locale translations\n"; \
	\
	echo "\tuninstall-locale"; \
	echo "\t\t- Remove Gettext translation files from system\n"; \
	\
	echo "\tinstall-man"; \
	echo "\t\t- Install & compress manual page(s)\n"; \
	\
	echo "\tuninstall-man"; \
	echo "\t\t- Uninstall Debreate manual page(s)\n"; \
	\
	echo "\tinstall-mime"; \
	echo "\t\t- Register MimeType information for Debreate"; \
	echo "\t\t  projects"; \
	echo "\t\t- Calls `tput bold`install-icons`tput sgr0`\n"; \
	\
	echo "\tuninstall-mime"; \
	echo "\t\t- Unregister Debreate project MimeType"; \
	echo "\t\t  information"; \
	echo "\t\t- Calls `tput bold`uninstall-icons`tput sgr0`\n"; \
	\
	echo "\tinstall-packages"; \
	echo "\t\t- Install Debreate's Python packages"; \
	echo "\t\t- Called by `tput bold`install`tput sgr0`\n"; \
	\
	echo "\tinstall-templates"; \
	echo "\t\t- Install template files used by application\n"; \
	\
	echo "\tdist"; \
	echo "\t\t- Create a source distribution package\n"; \
	\
	echo "\tdoc-html"; \
	echo "\t\t- Build Doxygen HTML files in docs/doxygen"; \
	echo "\t\t- Requires `tput bold`doxygen`tput sgr0` command (apt install doxygen)\n"; \
	\
	echo "\tdoxygen-format"; \
	echo "\t\t- Build Doxygen HTML files & add customizations"; \
	echo "\t\t- Calls `tput bold`doc-html`tput sgr0`\n"; \
	\
	echo "\tlocale"; \
	echo "\t\t- Build locale translations"; \
	echo "\t\t- Requires `tput bold`gettext`tput sgr0` command\n"; \
	\
	echo "\tdebianize"; \
	echo "\t\t- Configure source for building a Debian package"; \
	echo "\t\t  (not necessary, should already be configured)"; \
	echo "\t\t- Uses `tput bold`dh_make`tput sgr0` command (apt install dh-make)\n"; \
	\
	echo "\tdeb-bin"; \
	echo "\t\t- Build a Debian (.deb) package for installation"; \
	echo "\t\t- Uses `tput bold`debuild`tput sgr0` command (apt install devscripts)\n"; \
	\
	echo "\tdeb-bin-signed"; \
	echo "\t\t- Build a Debian (.deb) package for installation"; \
	echo "\t\t  & sign the .changes file"; \
	echo "\t\t- Uses `tput bold`debuild`tput sgr0` command (apt install devscripts)\n"; \
	\
	echo "\tdeb-src"; \
	echo "\t\t- Create a source distribution package with"; \
	echo "\t\t  Debian .dsc, .build, & .changes files"; \
	echo "\t\t- Uses `tput bold`debuild`tput sgr0` command (apt install devscripts)\n"; \
	\
	echo "\tdeb-src-signed"; \
	echo "\t\t- Create a source distribution package & sign"; \
	echo "\t\t  the .changes file for upload to a repository"; \
	echo "\t\t- Uses `tput bold`debuild`tput sgr0` command (apt install devscripts)\n"; \
	\
	echo "\tclean"; \
	echo "\t\t- Delete Debreate binary & any compiled Python"; \
	echo "\t\t  bytecode (.pyc) from the working directory\n"; \
	\
	echo "\tdistclean"; \
	echo "\t\t- Run `tput bold`clean`tput sgr0`, `tput bold`deb-clean`tput sgr0`, & delete compressed"; \
	echo "\t\t  distribution package archive\n"; \
	\
	echo "\tdoc-clean"; \
	echo "\t\t- Delete Doxygen HTML files from docs/doxygen.\n"; \
	\
	echo "\tlocale-clean"; \
	echo "\t\t- Clean compiled locale files from source\n"; \
	\
	echo "\tdeb-clean"; \
	echo "\t\t- Delete files created by `tput bold`debuild`tput sgr0`\n"; \
	\
	echo "Environment Variables:"; \
	\
	echo "\tprefix"; \
	echo "\t\t- Target prefix under which files will be installed"; \
	echo "\t\t- Default is /usr/local\n"; \
	\
	echo "\tDESTDIR"; \
	echo "\t\t- Prepends a target directory to prefix"; \
	echo "\t\t- Files will be installed under DESTDIR\prefix"; \
	echo "\t\t- DESTDIR is not written to the `tput bold`$(PACKAGE)`tput sgr0`"; \
	echo "\t\t  executable so it will not be able to find the"; \
	echo "\t\t  `tput bold`init.py`tput sgr0` script"; \
	echo "\t\t- If used with `tput bold`uninstall`tput sgr0` it must match that of"; \
	echo "\t\t  the `tput bold`install`tput sgr0` invocation\n"; \
	\
	echo "Notes on Environment Variables:"; \
	\
	echo "\tCurrently Debreate does not use a build setup system (such as"; \
	echo "\tGNU Autotools or CMake), so the \"prefix\" variable is static."; \
	echo "\tThis means that when calling `tput bold`make uninstall`tput sgr0`, \"prefix\" must"; \
	echo "\tbe set to the same as it was for `tput bold`make install`tput sgr0`. The same goes"; \
	echo "\tfor the \"DESTDIR\" variable.\n"; \
	\
	echo "\tE.g. if `tput bold`make install prefix=/usr`tput sgr0` was called, then `tput bold`make"; \
	echo "\tuninstall prefix=/usr`tput sgr0` must be called to uninstall.\n"; \
