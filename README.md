# usb2container

offer a way binding specific USB devices to container

## usage
with command:

```bash
usb2container start
```

with docker:

```bash
docker run -d --privileged \
    -p 29410:9410 \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /usr/bin/docker:/bin/docker \
    -v /run/udev:/run/udev:ro \
    --name usb2container \
    --restart always \
    williamfzc/usb2container
```

## license

[MIT](LICENSE)
