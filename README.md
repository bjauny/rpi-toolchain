# rpi-toolchain
This is intented to be a conan recipe to provide a cross-compile toolchain for RaspberryPi boards.

## Versions supported
The list of supported toolchains currently supported is:
- arm-gnu-toolchain-12.2.rel1-x86_64-arm-none-eabi (RPi1)

## Conan profiles
The needed profiles are all listed in the `profiles` folder.

## Usage
To build the package locally and have it available for your other recipes, use the following command:

```conan create . -pr:b=default -pr:h=./profiles/arm-none-eabi-target --build-require```

The profile can be relocated anywhere, just make sure to update the path in the build command.

## Further additions
More toolchains can be added if need be.