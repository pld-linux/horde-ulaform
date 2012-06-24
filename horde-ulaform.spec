%define	_hordeapp ulaform
%define	_snap	2005-09-17
#define	_rc		rc1
%define	_rel	0.3
#
%include	/usr/lib/rpm/macros.php
Summary:	A form generation/processing tool
Summary(pl):	Narz�dzie do generowania/przetwarzania formularzy
Name:		horde-%{_hordeapp}
Version:	0.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2+
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	594c1be0d7177e97019de58e27a9be02
Source1:	%{name}.conf
URL:		http://www.horde.org/ulaform/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Obsoletes:	%{_hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}

%description
Ulaform is a PHP-based dynamic HTML form creation and generation
system. Ulaform allows users to create sophisticated forms using a web
browser, and then render the forms within other web pages by a simple
PHP include inside a <?php ... ?> tag, or in other Horde applications
through the Horde Block API. Ulaform is intended to replace other
dynamic form generation techniques (such as FrontPage forms which
require the FrontPage extensions on the server, or CGI scripts which
require some programming ability).

Ulaform is based on the Horde_Form library of the Horde framework.
This gives it some useful capabilities: the ability to automatically
validate data, using JavaScript if available (or re-rendering of the
form if not); the ability to use GET or POST transparently; and
others.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Ulaform) please visit <http://www.horde.org/>.

%description -l pl
Ulaform to oparty na PHP system tworzenia i generowania dynamicznych
formularzy HTML. Pozwala u�ytkownikom tworzy� wymy�lne formularze
przy u�yciu przegl�darki WWW, a nast�pnie wy�wietla� formularze na
innych stronach WWW poprzez prost� dyrektyw� include PHP wewn�trz
znacznika <?php ... ?> lub w innych aplikacjach Horde poprzez API
Horde Block. Ulaform ma za zadanie zast�pi� inne techniki generowania
dynamicznych formularzy (takie jak formularze FrontPage, wymagaj�ce
rozszerze� FrontPage na serwerze, czy skrypty CGI wymagaj�ce
umiej�tno�ci programowania).

Ulaform jest oparty na bibliotece Horde_Form ze szkieletu Horde. Daje
to troch� przydatnych cech: mo�liwo�� automatycznego sprawdzania
poprawno�ci danych, u�ywanie JavaScriptu je�li jest dost�pny (lub
ponowne odrysowywanie formularza, je�li nie), mo�liwo��
przezroczystego u�ywania GET lub POST itp.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wi�cej informacji (w��cznie z pomoc� dla
Ulaform) mo�na znale�� na stronie <http://www.horde.org/>.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

if [ "$1" = 1 ]; then
%banner %{name} -e <<-EOF
	IMPORTANT:
	If you are installing Ulaform for the first time, You may need to
	create the Ulaform database tables. To do so run:
	zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{_hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
