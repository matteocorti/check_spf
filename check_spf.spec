%define version          1.1.0
%define release          0
%define sourcename       check_spf
%define packagename      nagios-plugins-check-spf
%define nagiospluginsdir %{_libdir}/nagios/plugins

# No binaries in this package
%define debug_package    %{nil}

Summary:       A Nagios plugin to check if RedHat or Fedora system is up-to-date
Name:          %{packagename}
Version:       %{version}
Obsoletes:     check_spf <= 100
Release:       %{release}%{?dist}
License:       GPLv3+
Packager:      Matteo Corti <matteo@corti.li>
Group:         Applications/System
BuildRoot:     %{_tmppath}/%{packagename}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:           https://github.com/matteocorti/check_spf
Source:        https://github.com/matteocorti/%{sourcename}/releases/download/v%{version}/%{sourcename}-%{version}.tar.gz

# Fedora build requirement (not needed for EPEL{4,5})
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: perl(Readonly)

Requires: perl(Mail::SPF::Iterator)

Requires:      nagios-plugins
# Yum security plugin RPM:
#    Fedora             : yum-plugin-security (virtual provides yum-security)
#    Red Hat Enterprise : yum-security
# Requires:  yum-security

%description
A Nagios plugin to check SPF records

%prep
%setup -q -n %{sourcename}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor \
    INSTALLSCRIPT=%{nagiospluginsdir} \
    INSTALLVENDORSCRIPT=%{nagiospluginsdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name "*.pod" -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS Changes NEWS README.md TODO COPYING COPYRIGHT
%{nagiospluginsdir}/%{sourcename}
%{_mandir}/man1/%{sourcename}.1*

%changelog
* Thu May 12 2022  <matteo@corti.li> - 1.1.0-0
- Updates to 1.1.0

* Mon Apr 11 2022  <matteo@corti.li> - 1.0.0-0
- Updates to 1.0.0

* Thu Mar 12 2020  <matteo@corti.li> - 0.9.0-0
- Updates to 0.9.0
