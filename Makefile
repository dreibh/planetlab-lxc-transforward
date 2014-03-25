obj-m += transforward.o

KVER=$(shell uname -r)
ARCH=$(shell uname -m)

# Is there an easy way of fetching this automatically, short of mapping /etc/redhat-release
DIST=fc18

ifeq ($(wildcard /lib/modules/$(KVER)/build),) 
	KVER=3.10.12-100.$(DIST).$(ARCH)
endif

all:
	make -C /lib/modules/$(KVER)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(KVER)/build M=$(PWD) clean

install:
	install -D -m 755 transforward.ko /lib/modules/$(KVER)/net/transforward/transforward.ko
	mkdir -p /etc/modules-load.d
	install -m 644 transforward.conf /etc/modules-load.d/transforward.conf
	install -m 644 transforward.service /usr/lib/systemd/system/transforward.service
	install -m 755 transforward.init /usr/sbin/transforward.init
