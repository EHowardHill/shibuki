# Shibuki

## About

Shibuki is a dynamic proxy and load balancer for a network mesh - sort of like Kubernetes, but without the docker containers. The idea is for it to be used on a central server, on the same network as a large collection of smaller devices, each with a web API installed. Shibuki enables you to dynamically access these devices as if they were accessible on a single IP address.

## How to use

Just execute `app.py`, and you'll be good to go. Make sure to put your server IP addresses in `servers.txt`, and edit `config.json` in order to adjust what port you're listening for requests on.
