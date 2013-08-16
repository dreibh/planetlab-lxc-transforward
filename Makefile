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
