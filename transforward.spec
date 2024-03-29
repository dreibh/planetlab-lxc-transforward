%define name transforward
%define version 0.1
%define taglevel 12

### legacy from locally-built kernels, used to define these
# kernel_release : 1.fc16  (24 is then the planetlab taglevel)
# kernel_version : 3.3.7
# kernel_arch :    i686 | x86_64

# when no custom kernel is being built, kernel_version is defined but empty
%define _with_planetlab_kernel %{?kernel_version:1}%{!?kernel_version:0}
%if ! %{_with_planetlab_kernel}

# compute these with "rpm -q --qf .. kernel-devel" when with the stock kernel
# this line below
#%define module_release %( rpm -q --qf "%{version}" kernel-devel )
# causes recursive macro definition no matter how much you quote

%define percent %
%define braop \{
%define bracl \}
%define kernel_version %( rpm -q --qf %{percent}%{braop}version%{bracl} kernel-devel )
%define kernel_release %( rpm -q --qf %{percent}%{braop}release%{bracl} kernel-devel )
%define kernel_arch %( rpm -q --qf %{percent}%{braop}arch%{bracl} kernel-devel )
%endif

# this is getting really a lot of stuff, could be made simpler probably
%define release %{kernel_version}.%{kernel_release}.%{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

%define kernel_id %{kernel_version}-%{kernel_release}.%{kernel_arch}
%define kernelpath /usr/src/kernels/%{kernel_id}


Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %{SCMURL}
Requires: kernel = %{kernel_version}-%{kernel_release}

Summary: Kernel module that transparently forwards ports between containers
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System Environment/Kernel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: transforward-%{version}.tar.gz
Requires: kernel = %{kernel_version}-%{kernel_release}

%description
Kernel module that transparently forwards ports between containers

%prep
%setup -q

%build
make -C %{kernelpath} V=1 M=$(pwd) KVER=%{kernel_id} modules

%install
install -D -m 755 transforward.ko $RPM_BUILD_ROOT/lib/modules/%{kernel_id}/net/transforward/transforward.ko
install -D -m 644 transforward.conf $RPM_BUILD_ROOT/etc/modules-load.d/transforward.conf
install -D -m 644 transforward.service $RPM_BUILD_ROOT/usr/lib/systemd/system/transforward.service
install -D -m 755 transforward.init $RPM_BUILD_ROOT/usr/sbin/transforward.init

%clean
rm -rf $RPM_BUILD_ROOT

%files
/lib/modules/%{kernel_id}
/etc/modules-load.d/transforward.conf
/usr/lib/systemd/system/transforward.service
/usr/sbin/transforward.init

%post
/sbin/depmod -a %{kernel_id}
/bin/systemctl enable transforward.service

%postun

%changelog
* Mon Jan 07 2019 Thierry <Parmentelat> - transforward-0.1-12
- tweaks for building against f27
- will no longer build against f29 though, because since kernel 4.19, the jprobe api has gone entirely
- # https://github.com/torvalds/linux/commit/4de58696de076d9bd2745d1cbe0930635c3f5ac9

* Sun Jul 16 2017 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-11
- no glock.h in kernel 4.9

* Sun Jul 10 2016 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-10
- fix to compile against linux 4.6 under f24

* Fri Apr 03 2015 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-9
- only cleaned up the systemd unit file to remove ControlGroup:

* Wed Feb 18 2015 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-8
- add a requirement to the right kernel rpm

* Wed Jul 16 2014 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-7
- tweak for building against a home-made kernel

* Mon Apr 28 2014 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-6
- change to specfile so depmod gets called with the right kernel version

* Fri Mar 21 2014 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-5
- harmless (changed default build kernel to the latest kernel in use)

* Wed Aug 28 2013 Sapan Bhatia <sapanb@cs.princeton.edu> - transforward-0.1-4
- * Bug fixes, which should lead to increased stability
- * Install via make and make install

* Mon Jul 09 2012 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - transforward-0.1-2
- load module at boot-time
- various tweaks, remove debugging statements
