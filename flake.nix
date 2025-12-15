{
  description = "TTS OU Project Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    diagrams-mmd.url = "github:andre-amorim/diagrams-mmd";
  };

  outputs = { self, nixpkgs, flake-utils, diagrams-mmd }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mermaid-cli = diagrams-mmd.packages.${system}.default;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            git
            coreutils
            nixfmt-rfc-style
            # Python Tools
            python314
            uv
            # Documentation Tools
            mermaid-cli
          ];

          shellHook = ''
            export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
            export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            echo "Environment Agent: Active"
            echo "Reproducible environment for TTS OU loaded."
          '';
        };
      }
    );
}
