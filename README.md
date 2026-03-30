# 💬 BiteWire
![Version](https://img.shields.io/badge/version-1.2.0-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Downloads](https://img.shields.io/github/downloads/Ziggx5/BiteWire/total)
![Client](https://img.shields.io/badge/component-client-blue)
![Server](https://img.shields.io/badge/component-server-green)

BiteWire is a simple, secure chat application that allows users to connect to hosted servers, communicate in real-time, and manage their own server through a dedicated server application.

---
<img width="2050" height="1166" alt="image" src="https://github.com/user-attachments/assets/739d7fd9-0331-481a-b9bb-69e7f64af4ca" />

## ⚙️ Server Setup

To host a BiteWire server, an SSL certificate is required for encrypted connections.
Example of a self-signed certificate:

```bash
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365
```

<img width="530" height="658" alt="image" src="https://github.com/user-attachments/assets/76866ef6-95a6-44a2-b5f4-91d5b6b0695b" />


## 📦 Downloads

<table>
  <tr>
    <th> / </th>
    <th>Windows (.exe)</th>
    <th>Debian (.deb)</th>
    <th>Red Hat (.rpm)</th>
  </tr>
  <tr>
    <td>BiteWire 1.2.0</td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/1.2.0/BiteWire.exe">⬇️ Download</a></td>
    <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/1.2.0/bitewire_1.2.0-3_amd64.deb">⬇️ Download</a></td>
      <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/1.2.0/bitewire-1.2.0-3.x86_64.rpm">⬇️ Download</a></td>
  </tr>
  <tr>
  <td>BiteWire Server 1.1.0</td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.1.0/BiteWire.Server.exe">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.1.0/bitewire-server_1.1.0-2_amd64.deb">⬇️ Download</a></td>
  <td><a href = "https://github.com/Ziggx5/BiteWire/releases/download/s1.1.0/bitewire-server-1.1.0-2.x86_64.rpm">⬇️ Download</a></td>
  </tr>
</table>

## ⚠️ Disclaimer

This project is still in an early stage of development.

Bugs and missing features may be present.

## ⭐ Support

If you like the project, consider giving it a star ⭐
