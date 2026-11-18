<div align="center">

# Minecraft Bedrock ORE-UI RCE

### A code execution issue hiding in plain sight

[![Research](https://img.shields.io/badge/type-security%20research-8B5CF6?style=for-the-badge)](#-overview)
[![Target](https://img.shields.io/badge/target-Minecraft%20Bedrock-62B47A?style=for-the-badge)](#-affected-component)
[![Version](https://img.shields.io/badge/version-1.26.53.2%20or%20lower-EF4444?style=for-the-badge)](#-affected-component)
[![Status](https://img.shields.io/badge/status-responsible%20disclosure-F59E0B?style=for-the-badge)](#-disclosure)

</div>

---

> A defensive proof of concept and research notes for a remote code execution issue associated with the ORE-UI component in Minecraft Bedrock.

## Overview

This repository documents research into a potential **remote code execution (RCE)** issue associated with the **ORE-UI** component in Minecraft Bedrock.

The purpose of this project is to support security education, controlled validation, and responsible disclosure. The PoC is intentionally scoped for isolated and authorized environments only.

## Affected component

- **Product:** Minecraft Bedrock

- **Component:** ORE-UI

- **Issue class:** Remote Code Execution (RCE)

- **Affected versions:** **1.26.53.2 and below**

- **Research focus:** Defensive analysis and controlled proof of concept

> **Version notice:** This PoC is intended for **Minecraft Bedrock 1.26.53.2 or lower**. Newer versions are outside the tested scope and may not be affected.

## Demonstration

The video below demonstrates the PoC in a controlled environment.

<video src="./demo.mp4" controls muted loop width="720"></video>

If the embedded player is not displayed, open the [demo video](./demo.mp4) directly.

## Impact

Under specific conditions, the issue may allow unintended code execution in the context of the affected environment. The practical impact depends on the version, configuration, attack surface, and privileges available to the affected process.

Potential security consequences may include:

- Execution of unauthorized code

- Compromise of application integrity

- Exposure of local data available to the affected process

- Further compromise if the process has excessive privileges

## Proof of concept

The PoC is designed to demonstrate the security impact in a controlled environment without providing a weaponized payload or instructions for attacking third-party systems.

Before testing:

1. Use an isolated test environment.

1. Do not use real accounts, personal data, or production systems.

1. Test only software and devices you own or are explicitly authorized to assess.

1. Remove or disable network access where it is not required.

1. Preserve logs and document the exact version and configuration used.

## Reproduction scope

Detailed reproduction material should be used only in an authorized lab. This repository does not provide persistence mechanisms, destructive actions, credential theft, evasion techniques, or deployment instructions against third-party systems.

## Disclosure

This research should be coordinated with the affected vendor or project before public release. Users should follow official advisories and apply available patches or mitigations as soon as they are published.

## Attribution

This repository documents related research. **I was not the original creator of the Minecraft Bedrock ORE-UI vulnerability.** Credit should be given to the original discoverer and any researchers whose work this PoC builds upon.

## Disclaimer

This project is provided for educational and defensive security research purposes only. Do not use it to compromise accounts, devices, servers, applications, or infrastructure without explicit authorization.

The author is not responsible for misuse, damage, data loss, service disruption, or unauthorized activity resulting from this material.

## License

Unless stated otherwise, the documentation in this repository is provided for educational purposes. Review and define an appropriate license before publishing source code or third-party materials.

---

<div align="center">

**Research responsibly. Test locally. Disclose carefully.**

</div>
