# Client run: 1.6.3+26.3

**FAIL** — exit timeout after 1200 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[11:01:42] [main/INFO]: Loading 138 mods:
```

## Harness

```
```

## Errors and warnings worth reading (13)

```
[11:01:45] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[11:01:45] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[11:01:54] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[11:01:55] [Render thread/INFO]: [STDERR]: Failed to probe max sources count, falling back to default value.
[11:01:55] [Render thread/INFO]: [STDERR]: java.lang.RuntimeException: Open device failed: Invalid value.
[11:01:57] [Render thread/ERROR]: Failed to create backend OpenGL
com.mojang.renderpearl.api.device.BackendCreationException: Failed to create window for OpenGL context: Installed Vulkan doesn't implement the VK_KHR_surface extension
[11:01:57] [Render thread/ERROR]: Failed to create backend Vulkan
com.mojang.renderpearl.api.device.BackendCreationException: Vulkan is not supported: Installed Vulkan doesn't implement the VK_KHR_surface extension
```
