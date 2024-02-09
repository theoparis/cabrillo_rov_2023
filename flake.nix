{
	inputs = {
		nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
		ros-overlay = {
			url = "https://code.theoparis.com/theoparis/nix-ros-overlay/archive/develop.tar.gz";
			inputs.nixpkgs.follows = "/nixpkgs";
		};
	};

	outputs = inputs@{
		self,
		nixpkgs,
		ros-overlay,
	}: let
		pkgs = import nixpkgs {
			system = "x86_64-linux";
		};

		rosPackages = ros-overlay.legacyPackages.x86_64-linux.humble;
	in {
		devShells.x86_64-linux.default = pkgs.mkShell {
			buildInputs = [
				rosPackages.colcon
				rosPackages.python3Packages.rosdep
				rosPackages.qt-gui
				pkgs.gnumake
			];
		};
	};
}
