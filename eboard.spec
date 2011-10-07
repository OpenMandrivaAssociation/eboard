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

