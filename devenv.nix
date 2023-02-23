{pkgs, ...}: {
  packages = [pkgs.zlib pkgs.stdenv.cc.cc.lib pkgs.python310Packages.faiss];
  languages.python = {
    enable = true;
    poetry.enable = true;
  };
  pre-commit.hooks.black.enable = true;
}
