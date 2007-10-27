# TODO: kill -O overriding our optflags
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Sunbird - standalone calendar application
Summary(pl.UTF-8):	Mozilla Sunbird - samodzielny kalendarz
Name:		mozilla-sunbird
Version:	0.7
Release:	0.4
License:	MPL/LGPL
Group:		X11/Applications/Networking
#Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/calendar/sunbird/releases/%{version}/source/lightning-sunbird-%{version}-source.tar.bz2
Source0:	lightning-sunbird-%{version}-20071027-source.tar.bz2
# Source0-md5:	7bc573958c75630962a121d7ed12eb6f
Source1:	%{name}.sh
Patch0:		mozilla-install.patch
URL:		http://www.mozilla.org/projects/sunbird/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	freetype-devel
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnomeui-devel >= 2.2.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3-3
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
#Requires:	%{name}-lang-resources = %{version}
Requires:	cairo >= 1.2.0
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# firefox/thunderbird/seamonkey/sunbird provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkxtbin.so libxpcom_compat.so libxpcom_core.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov		libgtkembedmoz.so libmozjs.so libxpcom.so
# and as we don't provide them, don't require either
%define		_noautoreq		libgtkembedmoz.so libmozjs.so libxpcom.so

%define		specflags	-fno-strict-aliasing

%description
The Sunbird Project is a cross platform standalone calendar
application based on Mozilla's XUL user interface language.

%description -l pl.UTF-8
Projekt Sunbird to wieloplatformowa aplikacja bedąca samodzielnym
kalendarzem, oparta na języku interfejsu użytkownika XUL.

%prep
%setup -q -c
cd mozilla
%patch0 -p1

%build
cd mozilla
cat << 'EOF' > .mozconfig
# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --disable-optimize
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --enable-optimize="%{rpmcflags}"
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}
ac_add_options --disable-freetype2
ac_add_options --disable-logging
ac_add_options --disable-updater
ac_add_options --disable-old-abi-compat-wrappers
ac_add_options --enable-application=calendar
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-elf-dynstr-gc
ac_add_options --enable-image-decoders=all
ac_add_options --enable-image-encoders=all
ac_add_options --enable-ipcd
ac_add_options --enable-ldap-experimental
ac_add_options --enable-native-uconv
ac_add_options --enable-safe-browsing
ac_add_options --enable-storage
ac_add_options --enable-system-cairo
ac_add_options --enable-url-classifier
ac_add_options --enable-xft
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-java-bin-path=/usr/bin
ac_add_options --with-java-include-path=/usr/include
ac_add_options --with-qtdir=/usr
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} -C mozilla/obj-%{_target_cpu}/xpinstall/packager stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/js $RPM_BUILD_ROOT%{_datadir}/%{name}/js
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/js $RPM_BUILD_ROOT%{_libdir}/%{name}/js
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/$(name=%{name}; echo ${name#mozilla-})

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
for d in chrome defaults extensions greprefs icons js res; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

#%post
#%{_sbindir}/firefox-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/sunbird

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt

%{_libdir}/%{name}/LICENSE
%{_libdir}/%{name}/README.txt

%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/m*
%attr(755,root,root) %{_libdir}/%{name}/s*
%attr(755,root,root) %{_libdir}/%{name}/reg*
%attr(755,root,root) %{_libdir}/%{name}/x*

%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/js
%{_datadir}/%{name}/res
%dir %{_datadir}/%{name}/extensions
# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_datadir}/%{name}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}

#%{_pixmapsdir}/*
#%{_desktopdir}/*

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/js
%{_libdir}/%{name}/res
