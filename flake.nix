{
  description = "Flake for Be Bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = system: nixpkgs.legacyPackages.${system};
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          pythonEnv = pkgs.python3.withPackages (ps: [
            ps.aiogram
            ps.aiohttp-socks
            ps.python-dotenv
          ]);
        in
        {
          bebot = pkgs.stdenv.mkDerivation {
            pname = "bebot";
            version = "0.1.0";
            src = pkgs.lib.cleanSource ./.;

            nativeBuildInputs = [ pkgs.makeWrapper ];

            installPhase = ''
              mkdir -p $out/libexec/bebot $out/bin
              cp -r . $out/libexec/bebot/

              makeWrapper ${pythonEnv}/bin/python $out/bin/bebot \
                --add-flags "$out/libexec/bebot/main.py"
            '';
          };
          default = self.packages.${system}.bebot;
        }
      );

      nixosModules.default = { config, lib, pkgs, ... }:
        let
          cfg = config.services.bebot;
          bebotPkg = self.packages.${pkgs.system}.bebot;
        in
        {
          options.services.bebot = {
            enable = lib.mkEnableOption "Be Bot service";

            tokenFile = lib.mkOption {
              type = lib.types.path;
              description = "Path to the file containing the Telegram Bot API token.";
            };

            settings = lib.mkOption {
              type = lib.types.attrsOf lib.types.str;
              default = { };
              description = "Environment variables passed to the bot service.";
            };
          };

          config = lib.mkIf cfg.enable {
            users.users.bebot = {
              isSystemUser = true;
              group = "bebot";
              description = "Be Bot service user";
            };

            users.groups.bebot = { };

            systemd.services.bebot = {
              description = "Be Bot";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];

              environment = cfg.settings;

              serviceConfig = {
                User = "bebot";
                Group = "bebot";
                Restart = "always";
                RestartSec = "5s";

                LoadCredential = [ "bot_token:${cfg.tokenFile}" ];

                ProtectSystem = "strict";
                ProtectHome = true;
                PrivateTmp = true;
                NoNewPrivileges = true;
              };

              script = ''
                if [ -f "$CREDENTIALS_DIRECTORY/bot_token" ]; then
                  export TOKEN="$(cat "$CREDENTIALS_DIRECTORY/bot_token")"
                fi
                exec ${bebotPkg}/bin/bebot
              '';
            };
          };
        };
    };
}
