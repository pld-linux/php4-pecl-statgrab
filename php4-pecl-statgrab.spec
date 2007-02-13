%define		_modname	statgrab
%define		_smodname	Statgrab
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - libstatgrab bindings
Summary(pl.UTF-8):	%{_modname} - dowiązania biblioteki libstatgrab
Name:		php4-pecl-%{_modname}
Version:	0.6.0
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	5e8e659e28d95da57c3d5a694cfb5af4
URL:		http://pecl.php.net/package/statgrab/
BuildRequires:	libstatgrab-devel >= 0.10
BuildRequires:	php4-devel >= 3:4.3.0
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libstatgrab is a library that provides a common interface for
retrieving a variety of system statistics on a number of *NIX like
systems.

This extension allows you to call the functions made available by
libstatgrab library.

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
libstatgrab to biblioteka dostarczająca wspólny interfejs do
odczytywania różnych statystyk systemowych na wielu systemach
uniksowych.

To rozszerzenie pozwala wywoływać funkcje udostępniane przez
bibliotekę libstatgrab.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_smodname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_smodname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_smodname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
