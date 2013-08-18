obj-m += transforward.o

KVER=$(shell uname -r)
ARCH=$(shell uname -m)

# Is there an easy way of fetching this automatically, short of mapping /etc/redhat-release
DIST=fc18

ifeq ($(wildcard /lib/modules/$(KVER)/build),) 
	KVER=3.10.6-100.$(DIST).$(ARCH)
endif

all:
	make -C /lib/modules/$(KVER)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(KVER)/build M=$(PWD) clean

install:
	install -D -m 755 transforward.ko /lib/modules/$(KVER)/net/transforward/transforward.ko
	install -m 644 transforward.service /usr/lib/systemd/system/transforward.service
