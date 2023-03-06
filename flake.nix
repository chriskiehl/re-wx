{
  description = "re-wx";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nix-filter-src.url = "github:numtide/nix-filter";

  outputs = { nixpkgs, flake-utils, nix-filter-src, self }@inputs:
    let
      nix-filter = import inputs.nix-filter-src;
      overlay = final: prev: {
        python3 = prev.python3.override {
          packageOverrides = pfinal: pprev: {
          };
        };
      };

      perSystem = system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ overlay ];
          };
        in
        {
          # https://nixos.wiki/wiki/Python#mkShell
          devShell = pkgs.mkShell {
            name = "re-wx_shell";
            packages = [
              pkgs.pyright
              (pkgs.python3.withPackages (p: with p; [
                wxPython_4_2
                typing-extensions
                pytest
                # mypy-extensions
              ]))
            ];
            nativeBuildInputs = [
              # https://nixos.wiki/wiki/Packaging/Quirks_and_Caveats#GLib-GIO-Message:_Using_the_.27memory.27_GSettings_backend._Your_settings_will_not_be_saved_or_shared_with
              # pkgs.wrapGAppsHook
              pkgs.gdb
            ];
            # shellHook = ''
            #   PYTHONPATH=${jitpython}/${jitpython.sitePackages}
            #   '';
              # XDG_DATA_DIRS=$GSETTINGS_SCHEMA_PATH
            shellHook = ''
              echo "Python ${pkgs.python3.version}"
            '';
          };
        };
    in
    flake-utils.lib.eachDefaultSystem
      perSystem // { inherit overlay; };
}

