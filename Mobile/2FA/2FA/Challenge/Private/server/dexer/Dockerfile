FROM openjdk:8-jdk

# Set up Android SDK and NDK
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3-pip \
    && wget -q https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip -O android-sdk.zip \
    && unzip -q android-sdk.zip -d /usr/local/android-sdk \
    && rm android-sdk.zip \
    && yes | /usr/local/android-sdk/tools/bin/sdkmanager --licenses \
    && /usr/local/android-sdk/tools/bin/sdkmanager "platform-tools" "build-tools;30.0.3" "platforms;android-30" "ndk-bundle"

# Set environment variables
ENV ANDROID_HOME /usr/local/android-sdk
ENV ANDROID_NDK_HOME /usr/local/android-sdk/ndk-bundle
ENV PATH ${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools:${ANDROID_NDK_HOME}:${ANDROID_HOME}/build-tools/30.0.3


COPY . .
RUN chmod +x /compile.sh



# Copy source files
RUN pip install --no-cache-dir -r requirements.txt
# Set entrypoint
WORKDIR /code
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
