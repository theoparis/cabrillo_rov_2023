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

			overlays = [
				(final: prev: rec {
					python3 = final.python310;
					python3Packages = python3.pkgs;
					python = python3;
			    pythonPackages = python3Packages;
				})
			];
		};

		rosPackages = ros-overlay.legacyPackages.x86_64-linux.humble;
	in {
		devShells.x86_64-linux.default = pkgs.mkShell {
			nativeBuildInputs = [
				pkgs.gnumake
				pkgs.stdenv
			];

			buildInputs = [
				pkgs.ffmpeg
				pkgs.yaml-cpp
				pkgs.python3Packages.setuptools
				rosPackages.colcon
				rosPackages.python3Packages.rosdep
				rosPackages.qt-gui
				rosPackages.ament-cmake-auto
				rosPackages.ament-lint-auto
				rosPackages.urdf
				rosPackages.rosidl-default-generators
				rosPackages.std-msgs
				rosPackages.image-transport
				rosPackages.image-transport-plugins
				rosPackages.camera-calibration-parsers
				rosPackages.ros2cli
				rosPackages.ros2launch
			];

			shellHook = ''
			export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:${pkgs.yaml-cpp}/lib"
			alias build='colcon build --symlink'
			'';
		};
	};
}
