#!/bin/bash
# By Pytel

apt_dependencies="apt-dependencies.txt"

# Install apt dependencies
sudo apt-get update
if [ -f $apt_dependencies ]; then
    xargs sudo apt-get -y install < $apt_dependencies
fi

# libraries for ARM toolchain
links="648013231/libtinfo5_6.4-2_amd64.deb 648013227/libncurses5_6.4-2_amd64.deb 646633572/libaio1_0.3.113-4_amd64.deb"

for link in $links; do
    # Download libs
    curl -O http://launchpadlibrarian.net/$link
    # Install libs
    lib=$(echo $link | cut -d'/' -f2)
    sudo dpkg -i $lib
    if [ $? -ne 0 ]; then
        echo -e "Error: Failed to install $lib"
        exit 1
    fi
    # Remove libs
    rm $lib
done

# Install ARM toolchain

# Test if the toolchain is installed
arm-none-eabi-gcc --version
arm-none-eabi-g++ --version
arm-none-eabi-gdb --version
arm-none-eabi-size --version

echo -e "Done!"

# Sources:
# https://community.localwp.com/t/installation-failed-in-ubuntu-24-04-lts/42579/6
