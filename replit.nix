{pkgs}: {
  deps = [
    pkgs.libxcrypt
    pkgs.freetype
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.glibcLocales
  ];
}
