
%define _prefix	/usr

Name:			hheretic
Summary:		Hacked Heretic is a Linux port of Raven Games old shooter, Heretic
License:		GPL
Group:			Games/Arcade
Version:		0.2.3
Release:		1
URL:			http://hhexen.sourceforge.net//hheretic.html
Source:			http://sourceforge.net/projects/hhexen/files/hheretic/%{version}/%{name}-%{version}-src.tgz
Source1:		%{name}.png
Source90:		%{name}.rpmlintrc
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_mixer)
Requires:	TiMidity++

%description
Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic.

This is a new release of Dan's excellent Hacked Heretic, by the
authors of Hammer of Thyrion (Heretic II). We're applying fixes,
adding a few features, and ensuring it runs on most *nix operating
systems.

This package contains the OpenGL enabled binary.

%package sdl
Summary:	Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic
Group:		Games/Arcade

%description sdl
Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic.

This is a new release of Dan's excellent Hacked Heretic, by the
authors of Heretic II. We're applying fixes,
adding a few features, and ensuring it runs on most *nix operating
systems.

This package contains the sdl enabled binary.

%package shareware
Summary:	Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic
Group:		Games/Arcade
Requires:	%{name}

%description shareware
Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic.

Those without the full retail version of Heretic can still play the
shareware.


%prep
%setup -q -n %{name}-%{version}-src

%build
# compile the OpenGL version (hheretic-gl)
%configure \
	--with-audio=sdlmixer
%make %{?jobs:-j%{jobs}}

# compile the software version (hheretic-sdl)
%make clean
%configure \
	--disable-gl \
	--with-audio=sdlmixer
%make

%install
# wrapper startscript
%__install -dm 755 %{buildroot}%{_gamesbindir}
for i in gl sdl; do
	%{__cat} > %{name}-$i.sh << EOF
#!/bin/bash
if [ ! -f \$HOME/.hheretic/version-%{version} ]; then
	mkdir -p \$HOME/.hheretic

	# if shareware is installed create a link
	if [ -f %{_datadir}/games/%{name}/heretic.wad ]; then
		cd \$HOME/.hheretic
		ln -s %{_datadir}/games/%{name}/heretic.wad .
	fi
	touch version-%{version}
fi
cd \$HOME/.hheretic
%{_prefix}/games/%{name}-$i "\$@"
EOF

	%__install -m 755 %{name}-$i.sh \
		%{buildroot}%{_gamesbindir}
done

# install the gamedata
%__install -dm 755 %{buildroot}/%{_datadir}/games/%{name} \
	%{buildroot}%{_datadir}/games/%{name}

%__install -dm 755 %{buildroot}%{_prefix}/games/%{name}
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
for i in gl sdl; do
	# binaries
	%__install -m 755 %{name}-$i \
		%{buildroot}%{_prefix}/games

	# icon
	 %__install -m 644 %{SOURCE1} \
	 	%{buildroot}%{_datadir}/pixmaps/%{name}-$i.png
done

# install menu entry
%__install -dm 755 %{buildroot}%{_datadir}/applications
%{__cat} > %{name}-gl.desktop << EOF
[Desktop Entry]
Name=Hacked Heretic (OpenGL)
GenericName=Hacked Heretic (OpenGL)
Comment=Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic
Exec=%{name}-gl.sh
Icon=%{name}-gl
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%{__cat} > %{name}-sdl.desktop << EOF
[Desktop Entry]
Name=Hacked Heretic (SDL)
GenericName=Hacked Heretic (SDL)
Comment=Hacked Heretic is a Linux port of Raven Game's old shooter, Heretic
Exec=%{name}-sdl.sh
Icon=%{name}-sdl
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%__install -m 644 %{name}*.desktop \
	%{buildroot}%{_datadir}/applications

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog LICENSE TODO
%{_gamesbindir}/%{name}-gl.sh
%{_prefix}/games/%{name}-gl
%{_datadir}/pixmaps/%{name}-gl.png
%{_datadir}/applications/%{name}-gl.desktop

%files sdl
%defattr(-,root,root)
%{_gamesbindir}/%{name}-sdl.sh
%{_prefix}/games/%{name}-sdl
%{_datadir}/pixmaps/%{name}-sdl.png
%{_datadir}/applications/%{name}-sdl.desktop

%files shareware
%defattr(-,root,root)
# %doc README.sharewarewad
# %dir %{_datadir}/games/%{name}
# %{_datadir}/games/%{name}/*.wad

