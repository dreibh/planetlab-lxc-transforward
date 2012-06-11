%define name transforward
%define version 0.1
%define taglevel 1

### legacy from locally-built kernels, used to define these
# kernel_release, kernel_version and kernel_arch are expected to be set by the build to e.g.
# kernel_release : 24.onelab  (24 is then the planetlab taglevel)
# kernel_version : 2.6.27.57 | 2.6.32  (57 in the 27 case is the patch level)
# kernel_arch :    i686 | x86_64

# with the stock kernel
# this line below
#%define module_release %( rpm -q --qf "%{version}" kernel-headers )
# causes recursive macro definition no matter how much you quote
%define percent %
%define braop \{
%define bracl \}
%define kernel_version %( rpm -q --qf %{percent}%{braop}version%{bracl} kernel-headers )
%define kernel_release %( rpm -q --qf %{percent}%{braop}release%{bracl} kernel-headers )
%define kernel_arch %( rpm -q --qf %{percent}%{braop}arch%{bracl} kernel-headers )

# this is getting really a lot of stuff, could be made simpler probably
%define release %{kernel_version}.%{kernel_release}.%{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

%define kernel_id %{kernel_version}-%{kernel_release}.%{kernel_arch}
%define kernelpath /usr/src/kernels/%{kernel_id}


Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %{SCMURL}

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
make -C %{kernelpath} V=1 M=$(pwd) modules

%install
install -D -m 755 transforward.ko $RPM_BUILD_ROOT/lib/modules/%{kernel_id}/net/transforward/transforward.ko

%clean
rm -rf $RPM_BUILD_ROOT

%files
/lib/modules/%{kernel_id}

%post

%postun

%changelog
