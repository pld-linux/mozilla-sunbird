#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Sunbird
Summary(pl):	Mozilla Sunbird
Name:		mozilla-sunbird
Version:	0.3a2
Release:	0.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/sunbird-%{version}-source.tar.bz2
# Source0-md5:	7c7bb48d71e75828471eb7ae0187824c
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
BuildRequires:	nspr-devel >= 1:4.6.1-2
BuildRequires:	nss-devel >= 3.10.2
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
Requires:	nspr >= 1:4.6.1-2
Requires:	nss >= 3.10.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package devel
Summary:	Headers for developing programs that will use Mozilla Firefox
Summary(pl):	Mozilla Firefox - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.1-2
Obsoletes:	mozilla-devel

%description devel
Mozilla Firefox development package.

%description devel -l pl
Pliki nag³ówkowe przegl±darki Mozilla Firefox.

%package lang-en
Summary:	English resources for Mozilla Firefox
Summary(pl):	Anglojêzyczne zasoby dla przegl±darki Mozilla Firefox
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla Firefox.

%description lang-en -l pl
Anglojêzyczne zasoby dla przegl±darki Mozilla Firefox.

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

%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/firefox-chrome+xpcom-generate

%postun
if [ "$1" = "0" ]; then
	rm -rf %{_firefoxdir}/chrome/overlayinfo
	rm -f  %{_firefoxdir}/chrome/*.rdf
	rm -rf %{_firefoxdir}/components
	rm -rf %{_firefoxdir}/extensions
fi

%triggerpostun -- %{name} < 1.5
%banner %{name} -e <<EOF
NOTICE:
If you have problem with upgrade from old mozilla-firefox 1.0.x,
you should remove it first and reinstall %{name}-%{version}
EOF

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla*
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%dir %{_firefoxdir}/plugins
%attr(755,root,root) %{_firefoxdir}/plugins/*.so
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%dir %{_firefoxdir}/extensions
%dir %{_firefoxdir}/init.d
%attr(755,root,root) %{_firefoxdir}/*.so
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/reg*
%attr(755,root,root) %{_firefoxdir}/x*
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/*.jar
%{_firefoxdir}/chrome/*.manifest
# -chat subpackage?
#%{_firefoxdir}/chrome/chatzilla.jar
#%{_firefoxdir}/chrome/content-packs.jar
%dir %{_firefoxdir}/chrome/icons
%{_firefoxdir}/chrome/icons/default

# -dom-inspector subpackage?
%dir %{_firefoxdir}/extensions/inspector@mozilla.org
%{_firefoxdir}/extensions/inspector@mozilla.org/*

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
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/en-US.manifest
