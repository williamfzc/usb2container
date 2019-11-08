# usb2container

offer a way binding specific USB devices to container

## goal

It's hard for us to bind a specific USB device to a docker container which is also specific. As you can see, the recommended way (from [stackoverflow](https://stackoverflow.com/questions/24225647/docker-a-way-to-give-access-to-a-host-usb-or-serial-device)) to achieve is:

```bash
docker run -t -i --privileged -v /dev/bus/usb:/dev/bus/usb ubuntu bash
``` 

It will bind all the devices to this container. It's unsafe. Every containers were granted to operate all of them.

Another way is binding devices by devpath. It may looks like:

```bash
docker run -t -i --privileged -v /dev/bus/usb/001/002:/dev/bus/usb/001/002 ubuntu bash
```

or `--device` (better, no `privileged`):

```bash
docker run -t -i --device /dev/bus/usb/001/002 ubuntu bash
```

Much safer. But actually it is hard to know what the devpath of a specific device is.

**This repo aims at offering a easy way for developers to get devpath of devices.**

## usage

by default, it will start a http server on port 9410.

### start usb2container service

All the information can be accessed via HTTP request. So you should deploy HTTP server firstly. It is not difficult. 

#### normal way

```bash
pip install usb2container
```

start server:

```bash
usb2container start
```

or running on another port (eg: 9646):

```bash
usb2container start 9646
```

#### docker

```bash
docker run -d --privileged \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /run/udev:/run/udev:ro \
    --name usb2container \
    --restart always \
    --net=host \
    williamfzc/usb2container
```

because of `--net=host` (**it is necessary**), you can not use port mapping. if you wanna run it on another port, you may need to edit Dockerfile and build it by yourself.

### access via HTTP

if everything is fine, you will see:

```text
email-validator not installed, email fields will be treated as str.
To install, run: pip install email-validator
2019-11-08 07:50:03.861 | INFO     | pyudevmonitor.monitor:start:26 - udevadm process up
2019-11-08 07:50:03.863 | INFO     | usb2container.server:start:42 - usb2container ver 0.1.1
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:9410 (Press CTRL+C to quit)
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

plug USB devices in after starting server, and then send a request to get all the devices:

```bash
curl 127.0.0.1:9410/api/device
```

you can access all the connected devices' info:

```text
{
	"/devices/pci0000:00/0000:00:14.0/usb1/1-13": {
		"ACTION": "add",
		"DEVPATH": "/devices/pci0000:00/0000:00:14.0/usb1/1-13",
		"DEVTYPE": "usb_device",
		"DRIVER": "usb",
		"ID_BUS": "usb",
		"ID_FOR_SEAT": "xxxxx",
		"ID_MODEL": "xxxxx",
		"ID_MODEL_ID": "xxxxx",
		"ID_PATH": "xxxxx",
		"ID_PATH_TAG": "xxxxx",
		"ID_REVISION": "xxxxx",
		"ID_SERIAL": "xxxxx",
		"ID_SERIAL_SHORT": "xxxxx",
		"ID_USB_INTERFACES": "xxxxx",
		"ID_VENDOR": "xxxxx",
		"ID_VENDOR_ENC": "xxxxx",
		"ID_VENDOR_FROM_DATABASE": "",
		"ID_VENDOR_ID": "xxxxx",
		"INTERFACE": "",
		"MAJOR": "189",
		"MINOR": "119",
		"MODALIAS": "",
		"PRODUCT": "xxxxx",
		"SEQNUM": "xxxxx",
		"SUBSYSTEM": "usb",
		"TAGS": "",
		"TYPE": "0/0/0",
		"USEC_INITIALIZED": "xxxxx",
		"adb_user": "",
		"_empty": false,
		"DEVNAME": "/dev/bus/usb/001/120",
		"BUSNUM": "001",
		"DEVNUM": "120",
		"ID_MODEL_ENC": "xxxxx"
	},
    ...
}
```

and bind them to your containers. For example, you can see the DEVNAME of this device is `/dev/bus/usb/001/120`:

```bash
docker run -t -i --device /dev/bus/usb/001/120 ubuntu bash
```

## dependencies

- [pyudevmonitor](https://github.com/williamfzc/pyudevmonitor)
- [fastapi](https://github.com/tiangolo/fastapi)

## license

[MIT](LICENSE)
