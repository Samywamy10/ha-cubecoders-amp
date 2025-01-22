# Cubecoders AMP HA Integration

Integrates with [AMP](https://cubecoders.com/AMP) to create devices out of each game server, and then provides a number of entities per server.

## Installing 
Install to [HACS by adding a custom repository](https://www.hacs.xyz/docs/faq/custom_repositories/) and then including this repository. Then search `Cubecoders AMP` in HACS; restart Home Assistant, then add the `AMP` integration.

### Configuration options
| Property | Example |
| ------- | ------- |
| host | `http://192.168.86.194:8080` |
| username | <yourAmpAdminUsername> |
| password | <yourAmpAdminPassword> |
  

## Dependencies

Relies on [cc-ampapi](https://github.com/k8thekat/AMPAPI_Python)