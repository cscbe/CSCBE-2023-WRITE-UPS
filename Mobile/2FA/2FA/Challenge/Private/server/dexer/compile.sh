#!/bin/bash

mkdir -p /code/app/be/dauntless/twofa

# Decode base64 input
echo $1 | base64 -d > /code/app/be/dauntless/twofa/Vault.java

# Set up Android SDK environment variables
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# Compile Java source code to dex file
javac -classpath $ANDROID_HOME/platforms/android-30/android.jar /code/app/be/dauntless/twofa/Vault.java
dx --dex --output=Vault.dex /code/app

# Output dex file as base64-encoded string
cat Vault.dex | base64

rm Vault.dex
rm /code/app/be/dauntless/twofa/Vault.*