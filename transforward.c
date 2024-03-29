#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/types.h>
#include <linux/kernel.h>
#include <linux/fs_struct.h>
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/reboot.h>
#include <linux/delay.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <asm/uaccess.h>
#include <linux/sysrq.h>
#include <linux/timer.h>
#include <linux/time.h>
/*#include <linux/lglock.h>*/
#include <linux/init.h>
#include <linux/idr.h>
#include <linux/namei.h>
#include <linux/bitops.h>
#include <linux/mount.h>
#include <linux/dcache.h>
#include <linux/spinlock.h>
#include <linux/completion.h>
#include <linux/sched.h>
#include <linux/seq_file.h>
#include <linux/kprobes.h>
#include <linux/kallsyms.h>
#include <linux/nsproxy.h>
#include <net/sock.h>
#include <linux/inetdevice.h>

#define VERSION_STR "0.0.1"

#ifndef CONFIG_X86_64
#error "This code does not support your architecture"
#endif

MODULE_AUTHOR("Sapan Bhatia <sapanb@cs.princeton.edu>");
MODULE_DESCRIPTION("Transparent port forwarding for LXC.");
MODULE_LICENSE("GPL");
MODULE_VERSION(VERSION_STR);

struct proc_dir_entry *proc_entry;

static int address_in_root(unsigned int haddr) {
    struct net_device *dev;
    struct net *net = &init_net;

    for_each_netdev(net, dev) {
            unsigned int ifhaddr = inet_select_addr(dev,0,0);
            //printk(KERN_CRIT "Checking address: %u",ifhaddr);
            if (haddr == ifhaddr) return 1;
    }
    return 0;
}

static int inet_bind_entry(struct socket *sock, struct sockaddr *uaddr, int addr_len) {
    struct sockaddr_in *addr = (struct sockaddr_in *)uaddr;
    unsigned int snum = addr->sin_addr.s_addr;
	//printk(KERN_CRIT "Checking address %d",snum);
    if (address_in_root(snum)) {
        put_net(sock_net(sock->sk));
        sock_net_set(sock->sk, get_net(&init_net)); 
        //printk(KERN_CRIT "Rewiring netns");
    }
    jprobe_return();
    return 0;
}

static struct file *do_last_probe(struct nameidata *nd, struct path *path,
                         const struct open_flags *op, const char *pathname) {
    
    
    jprobe_return();

}

static struct jprobe net_probe = {
	.entry = (kprobe_opcode_t *) inet_bind_entry
};


static void __exit transforward_exit(void)
{
	unregister_jprobe(&net_probe);
	printk("Transforward: Stopped transforward.\n");
}

int once_only=0;

static int init_probes(void)
{
    int ret = 0;
	printk("Transforward: starting transforward version %s.\n",
	       VERSION_STR);
          net_probe.kp.addr = 
                  (kprobe_opcode_t *) kallsyms_lookup_name("inet_bind");
          if (!net_probe.kp.addr) {
                  printk("Couldn't find %s to plant kretprobe\n", "inet_bind");
                  return -1;
          }
  
          if ((ret = register_jprobe(&net_probe)) <0) {
                  printk("register_jprobe failed, returned %u\n", ret);
                  return -1;
          }

        return ret;
}

/*  as per http://www.tldp.org/LDP/lkmpg/2.4/html/c577.htm
    the declaration of write in the file_operations struct reads:
    ssize_t (*write) (struct file *, const char *, size_t, loff_t *);
*/
ssize_t procfile_write(struct file *file, const char *buffer, size_t count, loff_t *data) {		
	if (!once_only) {
		once_only=1;
		if (init_probes()==-1)
			printk(KERN_CRIT "Could not install procprotect probes. Reload module to retry.");
		else 
			printk(KERN_CRIT "Activated transforward module");
	}
    return count;
}
static const struct file_operations transforward_fops = {
    .owner = THIS_MODULE,
    .write = procfile_write
};

static int __init transforward_init(void)
{
    int ret = 0;
	printk("Transforward: starting transforward version %s.\n",
	       VERSION_STR);

    proc_entry = proc_create("transforward", 0644, NULL, &transforward_fops);
	return ret;
}

module_init(transforward_init);
module_exit(transforward_exit);
