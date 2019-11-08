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
    -v /dev/bus/usb:/dev/bus/usb \
    -v /run/udev:/run/udev:ro \
    --name usb2container \
    --restart always \
    --net=host \
    williamfzc/usb2container
```

## license

[MIT](LICENSE)
