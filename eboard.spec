%define name    eboard
%define version 1.1.1
%define release %mkrel 1

Summary:        FICS chess-server interface
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        GPLv2+
Group:          Games/Boards
URL:            http://eboard.sf.net
Source0:        http://nchc.dl.sourceforge.net/sourceforge/eboard/%name-%version.tar.bz2
Source1:        http://nchc.dl.sourceforge.net/sourceforge/eboard/%name-icons.tar.bz2
Source2:	http://nchc.dl.sourceforge.net/sourceforge/eboard/%name-extras-1pl2.tar.bz2
Source3:	http://nchc.dl.sourceforge.net/sourceforge/eboard/%name-extras-2.tar.bz2
Patch0:		eboard-1.0.4-mdv-fix-str-fmt.patch
Patch1:		eboard-1.1.1-gcc44.patch
Patch2:		eboard-1.1.1-libpng15.patch
Patch3:		eboard-1.1.1-link.patch
Patch4:		eboard-1.1.1-ldl.patch
BuildRoot:      %{_tmppath}/%{name}-buildroot
Buildrequires:  gtk+2-devel
Buildrequires:  libpng-devel

%description
eboard is a chess interface for Unix-like systems (GNU/Linux, FreeBSD,
Solaris, etc.) based on the GTK+ GUI toolkit.  It provides a chess
board interface to ICS (Internet Chess Servers) like FICS and to chess
engines like GNU Chess, Sjeng and Crafty.

%prep
%setup -q
%setup -q -T -D -a1
%setup -q -T -D -a2
%setup -q -T -D -a3
%patch0 -p1 -b .strfmt
%patch1 -p1 -b .gcc44
%patch2 -p0 -b .png15
%patch3 -p0 -b .link
%patch4 -p1 -b .ldl


%build
%configure2_5x

# o_O
%__sed -i 's/-O6/%{optflags}/' Makefile
%__sed -i 's,/usr/share,%{_gamesdatadir},' config.h


%make bindir=%{_gamesbindir} \
      datadir=%{_gamesdatadir}/%{name}

# Add the additional themes to the configurationfile
%__cat %{name}-extras-1pl2/extras1.conf >> %{name}_themes.conf
%__cat %{name}-extras-2/extras2.conf    >> %{name}_themes.conf

%install
%__rm -rf %{buildroot}
%makeinstall bindir=%{buildroot}%{_gamesbindir} \
             datadir=%{buildroot}%{_gamesdatadir}/%{name}

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Eboard
Comment=FICS chess-server interface
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Type=Application
Categories=Game;BoardGame;
EOF

# Icons
%__install -D %{name}-48x48.png %{buildroot}%{_liconsdir}/%{name}.png
%__install -D %{name}-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
%__install -D %{name}-16x16.png %{buildroot}%{_miconsdir}/%{name}.png

# extras
%__install -d %{buildroot}%{_gamesdatadir}/%{name}
%__install %{name}-extras-*/*.{png,wav} %{buildroot}%{_gamesdatadir}/%{name}


%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
%__rm -rf %{buildroot}

%files
%defattr(0755,root,root,0755)
%{_gamesbindir}/*
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING README ChangeLog TODO Documentation/*
%{_gamesdatadir}/%{name}/*
%dir %{_gamesdatadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man6/*
%{_datadir}/applications/*
%{_iconsdir}/*



%changelog
* Fri Oct 07 2011 Andrey Bondrov <abondrov@mandriva.org> 1.1.1-1mdv2012.0
+ Revision: 703478
- Add patch4 to fix linking with libdl
- New version: 1.1.1

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-6mdv2011.0
+ Revision: 610333
- rebuild

* Mon Dec 07 2009 Jérôme Brenier <incubusss@mandriva.org> 1.0.4-5mdv2010.1
+ Revision: 474486
- fix str fmt
- fix license tag

  + Thierry Vignaud <tv@mandriva.org>
    - use %%configure2_5x
    - rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.0.4-3mdv2009.0
+ Revision: 244604
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Feb 12 2008 Thierry Vignaud <tv@mandriva.org> 1.0.4-1mdv2008.1
+ Revision: 165938
- fix spacing at top of description
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Aug 19 2007 Funda Wang <fwang@mandriva.org> 1.0.4-1mdv2008.0
+ Revision: 66551
- xdg menu entry
- New vesion 1.0.4


* Tue Jan 16 2007 Lenny Cartier <lenny@mandriva.com> 1.0.2-1mdv2007.0
+ Revision: 109420
- Update to 1.0.2

* Tue Jan 09 2007 Lenny Cartier <lenny@mandriva.com> 1.0.1-1mdv2007.1
+ Revision: 106679
- Update to 1.0.1
- Buildrequires
- Adjust buildrequires
- Update to 1.0.0
- Import eboard

