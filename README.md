# SysML v1 MCP Bridge — Pro Extension

This repository contains the compiled pro-extension JAR for the SysML v1 MCP Bridge — Pro Extension.

## Contents

| File | Description |
|---|---|
| `jgs-sysmlv1-pro.jar` | Compiled pro-extension plugin JAR |
| `RELEASE-INFO.txt` | SHA-256 digest and staging metadata |

## Installation

Customers receive this JAR pre-packaged in their licence bundle (zip).
The bundle also contains `AGENT-INSTALL.md` with automated installation
instructions — the JAR is copied to:

```
<CATIA Magic install>\plugins\<plugin-dir>\jgs-pro\jgs-sysmlv1-pro.jar
```

**The free base plugin must be installed before the pro JAR.**
The pro JAR is loaded dynamically by the free plugin at startup via URLClassLoader;
it will silently fail to load if the free plugin is absent.

## Support

JG Systems Consulting Ltd.
