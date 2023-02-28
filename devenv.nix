{pkgs, ...}: {
  packages = [
    pkgs.zlib
    pkgs.stdenv.cc.cc.lib
    pkgs.python310Packages.faiss
    pkgs.python310Packages.nltk
    pkgs.python310Packages.lxml
    pkgs.nodePackages_latest.pyright
  ];
  languages.python = {
    enable = true;
    poetry.enable = true;
  };

  pre-commit.hooks.black.enable = true;

  processes = {
    web-server.exec = "uvicorn web.main:app --port 8080 --reload";
  };

  env.ROOT_DIR = "var";
}
