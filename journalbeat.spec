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
cd $RPM_BUILD_ROOT
tar xvvf %{SOURCE0}


%build
mkdir -p $RPM_BUILD_ROOT/go/src/github.com/mheese/
ln -s $RPM_BUILD_ROOT/%{name}-%{PKGVERSION} $RPM_BUILD_ROOT/go/src/github.com/mheese/journalbeat

#go build -ldflags "-s -w"
LDFLAGS="-s -w"
#export GOPATH=$RPM_BUILD_ROOT/go/
export GOROOT=$RPM_BUILD_ROOT/go/
%gobuild 
pwd
echo $RPM_BUILD_ROOT
ls -la

#for i in all api-store zookeeper; do
#sed -i 's@^ad.es.path.home=.*$@ad.es.path.home=/opt/apm/events-service/data@' conf/events-service-$i.properties
#sed -i 's@^ad.zookeeper.dataDir=.*$@ad.zookeeper.dataDir=/opt/apm/events-service/data@' conf/events-service-$i.properties
#done

%install
mkdir -p $RPM_BUILD_ROOT/etc/journalbeat
cp src/etc/journalbeat.yml $RPM_BUILD_ROOT/etc/journalbeat
mkdir $RPM_BUILD_ROOT/%{_sharedstatedir}/journalbeat

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}

%files
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/etc/journalbeat/journalbeat.yml
%dir %{_sharedstatedir}/journalbeat

%defattr(754,root,root,755)


%defattr(664,jboss,appengs,755)
%config(noreplace) %{_unitdir}/journalbeat.yml

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}

%changelog
* Wed Jul 19 2017 - fholzer@gvcgroup.com
- Initial release
