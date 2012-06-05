%define url $URL$

%define name transforward
%define version 0.1
%define taglevel 1

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %(echo %{url} | cut -d ' ' -f 2)

Summary: Kernel module that transparently forwards ports between containers
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System Environment/Kernel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: transforward-%{version}.tar.gz

%description
Kernel module that transparently forwards ports between containers

%prep 
%setup -q

%build
make -C /lib/modules/`ls /lib/modules | head -1`/build M=$PWD modules

%install
mkdir -p $RPM_BUILD_ROOT/lib/modules/`ls /lib/modules | head -1`/kernel/net/transforward
cp transforward.ko $RPM_BUILD_ROOT/lib/modules/`ls /lib/modules | head -1`/kernel/net/transforward

%clean
rm -rf $RPM_BUILD_ROOT

%files
/lib

%post

%postun

%changelog
