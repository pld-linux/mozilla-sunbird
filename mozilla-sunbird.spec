# TODO: kill -O overriding our optflags
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Sunbird - standalone calendar application
Summary(pl):	Mozilla Sunbird - samodzielny kalendarz
Name:		mozilla-sunbird
Version:	0.3
Release:	0.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/sunbird-%{version}.source.tar.bz2
# Source0-md5:	5579069a44e382bb963e3bbf6897a366
URL:		http://www.mozilla.org/projects/sunbird/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	freetype-devel
#BuildRequires:	heimdal-devel >= 0.7.1
#BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnomeui-devel >= 2.2.0
#BuildRequires:	libjpeg-devel >= 6b
#BuildRequires:	libpng-devel >= 1.2.7
#BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires:	%{name}-lang-resources = %{version}
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sunbirddir	%{_libdir}/mozilla-sunbird

%description
The Sunbird Project is a cross platform standalone calendar
application based on Mozilla's XUL user interface language.

%description -l pl
Projekt Sunbird to wieloplatformowa aplikacja bed±ca samodzielnym
kalendarzem, oparta na jêzyku interfejsu u¿ytkownika XUL.

%package devel
Summary:	Headers for developing programs that will use Mozilla Sunbird
Summary(pl):	Mozilla Sunbird - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.3
Obsoletes:	mozilla-devel

%description devel
Mozilla Sunbird development package.

%description devel -l pl
Pliki nag³ówkowe kalendarza Mozilla Sunbird.

%package lang-en
Summary:	English resources for Mozilla Sunbird
Summary(pl):	Anglojêzyczne zasoby dla kalendarza Mozilla Sunbird
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla Sunbird.

%description lang-en -l pl
Anglojêzyczne zasoby dla kalendarza Mozilla Sunbird.

%prep
%setup -q -n mozilla

%build
%configure2_13 \
	--enable-application=calendar

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}{,extensions}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/firefox-chrome+xpcom-generate

%postun
if [ "$1" = "0" ]; then
	rm -rf %{_sunbirddir}/chrome/overlayinfo
	rm -f  %{_sunbirddir}/chrome/*.rdf
	rm -rf %{_sunbirddir}/components
	rm -rf %{_sunbirddir}/extensions
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla*
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/*
%dir %{_sunbirddir}
%{_sunbirddir}/res
%dir %{_sunbirddir}/components
%attr(755,root,root) %{_sunbirddir}/components/*.so
%{_sunbirddir}/components/*.js
%{_sunbirddir}/components/*.xpt
%dir %{_sunbirddir}/plugins
%attr(755,root,root) %{_sunbirddir}/plugins/*.so
%{_sunbirddir}/searchplugins
%{_sunbirddir}/icons
%{_sunbirddir}/defaults
%{_sunbirddir}/greprefs
%dir %{_sunbirddir}/extensions
%dir %{_sunbirddir}/init.d
%attr(755,root,root) %{_sunbirddir}/*.so
%attr(755,root,root) %{_sunbirddir}/*.sh
%attr(755,root,root) %{_sunbirddir}/m*
%attr(755,root,root) %{_sunbirddir}/f*
%attr(755,root,root) %{_sunbirddir}/reg*
%attr(755,root,root) %{_sunbirddir}/x*
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_sunbirddir}/chrome
%{_sunbirddir}/chrome/*.jar
%{_sunbirddir}/chrome/*.manifest
# -chat subpackage?
#%{_sunbirddir}/chrome/chatzilla.jar
#%{_sunbirddir}/chrome/content-packs.jar
%dir %{_sunbirddir}/chrome/icons
%{_sunbirddir}/chrome/icons/default

# -dom-inspector subpackage?
%dir %{_sunbirddir}/extensions/inspector@mozilla.org
%{_sunbirddir}/extensions/inspector@mozilla.org/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*

%files lang-en
%defattr(644,root,root,755)
%{_sunbirddir}/chrome/en-US.jar
%{_sunbirddir}/chrome/en-US.manifest
