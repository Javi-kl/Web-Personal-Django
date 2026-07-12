{
  description = "Mi API";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python314                            
          ruff                                 
          basedpyright                         
          python314Packages.python-lsp-server  # LSP base para Helix
          python314Packages.python-lsp-ruff    # plugin ruff para el LSP
        ];

        shellHook = ''
          echo "🐍 $(python --version) | ruff $(ruff --version | cut -d' ' -f2) | basedpyright $(basedpyright --version)"
        '';
      };
    };
}
