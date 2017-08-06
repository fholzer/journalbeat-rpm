Name:		journalbeat
Version:	%{PKGVERSION}
Release:	%{PKGRELEASE}%{?dist}
Source0:	%{name}-v%{version}.tar.gz
Source1:        journalbeat.service
Summary:        Journalbeat is a log shipper from systemd/journald to Logstash/Elasticsearch
License:        proprietary
Packager:       %{packager}

ExclusiveArch:  %{go_arches}
BuildRequires:  golang

%{?systemd_requires}
BuildRequires:  systemd

%description


%prep
cd $RPM_BUILD_DIR
tar xvvf %{SOURCE0}
mkdir -p $RPM_BUILD_DIR/go/src/github.com/mheese/
mv $RPM_BUILD_DIR/%{name}-%{PKGVERSION} $RPM_BUILD_DIR/go/src/github.com/mheese/journalbeat

%build

cd $RPM_BUILD_DIR/go/src/github.com/mheese/journalbeat
export GOPATH=$RPM_BUILD_DIR/go/
GOOS=linux go build -ldflags="-s -w"

%install
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
cp $RPM_BUILD_DIR/go/src/github.com/mheese/journalbeat/journalbeat $RPM_BUILD_ROOT/%{_sbindir}

mkdir -p $RPM_BUILD_ROOT/etc/journalbeat
cp $RPM_BUILD_DIR/go/src/github.com/mheese/journalbeat/etc/journalbeat.yml $RPM_BUILD_ROOT/etc/journalbeat/

mkdir -p $RPM_BUILD_ROOT/%{_sharedstatedir}/journalbeat

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}

%files
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/journalbeat/journalbeat.yml
%config(noreplace) %{_unitdir}/journalbeat.service

%dir %{_sharedstatedir}/journalbeat

%defattr(754,root,root,755)
%{_sbindir}/journalbeat

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}

%changelog
* Wed Jul 19 2017 - fholzer@gvcgroup.com
- Initial release
