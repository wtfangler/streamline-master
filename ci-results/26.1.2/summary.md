# Client run: 1.4.3+26.1.2

**PASS** — exit joined after 59 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:36:43] [main/INFO]: Loading 126 mods:
```

## Metrics

| metric | value |
| --- | --- |

## Crashes

none

## Harness

```
```

## Errors and warnings worth reading (25)

```
[12:36:45] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:36:45] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:36:53] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:59)
Caused by: com.mojang.authlib.exceptions.MinecraftClientHttpException: Status: 401
[12:36:56] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.1.2/assets/objects/61/616e9e15e6bbed6f5a5beba38ee44ff19a9a0235
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.1.2/assets/objects/61/616e9e15e6bbed6f5a5beba38ee44ff19a9a0235
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:36:56] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.1.2/assets/objects/5d/5d4d95afbcabbdfbfc337ad4b2431eab240b617b
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.1.2/assets/objects/5d/5d4d95afbcabbdfbfc337ad4b2431eab240b617b
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:36:57] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:36:57] [Download-1/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:36:57] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:36:57] [IO-Worker-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:36:57] [IO-Worker-1/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:37:05] [Worker-ResourceReload-2/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
```
