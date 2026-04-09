# 💬 BiteWire
![Version](https://img.shields.io/badge/version-1.4.0-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Downloads](https://img.shields.io/github/downloads/Ziggx5/BiteWire/total)
![Client](https://img.shields.io/badge/component-client-blue)
![Server](https://img.shields.io/badge/component-server-green)

BiteWire is a simple, secure chat application that allows users to connect to hosted servers, communicate in real-time, and manage their own server through a dedicated server application.

---
<img width="2050" height="1166" alt="image" src="https://github.com/user-attachments/assets/06c55982-12e6-46bc-acea-e09e5c11dc08" />

## ⚙️ Server Setup

To host a BiteWire server, an SSL certificate is required for encrypted connections.
Example of a self-signed certificate:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365
```

<img width="530" height="658" alt="image" src="https://github.com/user-attachments/assets/1300fe65-f33d-4a3d-9f5d-33c32b26db1a" />


## 📦 Downloads

<table>
  <tr>
    <th> / </th>
    <th>Windows (.exe)</th>
    <th>Debian (.deb)</th>
    <th>Red Hat (.rpm)</th>
  </tr>
  <tr>
    <td>BiteWire 1.4.0</td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c1.4.0/BiteWire.exe">⬇️ Download</a></td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c1.4.0/bitewire_1.3.0_amd64.deb">⬇️ Download</a></td>
      <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/c1.4.0/bitewire-1.4.0-1.x86_64.rpm">⬇️ Download</a></td>
  </tr>
  <tr>
  <td>BiteWire Server 1.2.0</td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.2.0/BiteWire.Server.exe">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.2.0/bitewire-server_1.2.0_amd64.deb">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.2.0/bitewire-server-1.2.0-1.x86_64.rpm">⬇️ Download</a></td>
  </tr>
</table>

## ⚠️ Disclaimer

This project is still in an early stage of development.

Bugs and missing features may be present.

## ⭐ Support

If you like the project, consider giving it a star ⭐
