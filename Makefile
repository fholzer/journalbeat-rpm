PKGNAME=journalbeat
PKGVERSION=5.5.0
PKGRELEASE=1
#PKGROOT=events-service

all: build

prepare:
	mkdir -p rpmbuild/SOURCES
	mkdir -p rpmbuild/SPECS
	mkdir -p rpmbuild/SRPMS
	mkdir -p rpmbuild/RPMS
	mkdir -p rpmbuild/BUILD
	mkdir -p rpmbuild/BUILDROOT
	cp src/* rpmbuild/SOURCES
	cp $(PKGNAME).spec rpmbuild/SPECS
	wget -N "https://github.com/mheese/journalbeat/archive/v$(PKGVERSION).tar.gz" -O rpmbuild/SOURCES/$(PKGNAME)-v$(PKGVERSION).tar.gz

build: prepare
	rpmbuild -bb \
	-D "_topdir $(PWD)/rpmbuild" \
	-D "PKGVERSION $(PKGVERSION)" \
	-D "PKGRELEASE $(PKGRELEASE)" \
	-D "packager $(USER)@gvcgroup.com" \
	$(PKGNAME).spec

release: clean bumpRelease
	make build

bumpRelease:
	mv Makefile Makefile.bak
	awk '/^PKGRELEASE=[1-9][0-9]*/{n = substr($$0, match($$0, /[0-9]+/), RLENGTH) + 1; sub(/[0-9]+/, n); print; next} {print}' Makefile.bak >Makefile

clean:
	$(RM) -r rpmbuild
