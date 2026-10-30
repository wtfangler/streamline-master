# Client run: 1.5.2+26.2

**PASS** — exit 0 after 52 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:36:33] [main/INFO]: Loading 124 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 309.18 |
| startup_s | 33.43 |
| world_ready_s | 39.14 |

## Crashes

none

## Harness

```
[12:36:56] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: overlay net.minecraft.client.gui.screens.LoadingOverlay / screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:36:56] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_1
[12:36:57] [IO-Worker-1/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_2
[12:36:57] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_3
[12:37:05] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 199: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:37:05] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric startup_s 33.43
[12:37:05] [IO-Worker-7/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_1_LevelLoadingScreen
[12:37:05] [IO-Worker-7/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_2_LevelLoadingScreen
[12:37:06] [IO-Worker-7/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_3_LevelLoadingScreen
[12:37:06] [IO-Worker-7/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_4_LevelLoadingScreen
[12:37:08] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 259: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:37:11] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 298: screen none / in world
[12:37:11] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 39.14
[12:37:19] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 9 (software rendering in CI, not a benchmark)
[12:37:19] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 309.18
[12:37:19] [IO-Worker-7/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_3_ingame
[12:37:20] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 479: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:37:21] [IO-Worker-5/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_4_saving
[12:37:22] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (31)

```
[12:36:35] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:36:36] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:36:44] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[12:36:47] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:36:47] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:36:48] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:36:48] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:36:48] [Download-2/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:36:48] [Download-3/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:36:48] [Download-3/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
com.mojang.authlib.exceptions.MinecraftClientException: Failed to read from https://sessionserver.mojang.com/session/minecraft/profile/4548c590b3414acdbd0b2498f7e9079d?unsigned=false due to Read timed out
Caused by: java.net.SocketTimeoutException: Read timed out
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:36:56] [Worker-ResourceReload-1/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
[12:37:08] [Download-1/ERROR]: Failed to retrieve profile key pair
MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/certificates, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
```
