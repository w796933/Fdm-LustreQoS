# Feedback-driven-Monitor Lustre QoS TOOL
@(Feedback-driven-Monitor Lustre QoS TOOL)[Feedback-driven-Monitor Lustre QoS TOOL│HELP│Feedback-driven-Monitor]

**Feedback-driven-Monitor(Fdm) Lustre QoS TOOL** 是在[MULTEXU](https://github.com/ShijunDeng/multexu)基础上开发的，特别针对Feedback-driven-Monitor设计的自动安装、部署、测试、控制和监测的工具套件，包括以下功能：
 
- **认证** ：在一个局域网，在其中指定一台主机做为管理机，其它主机做为被管理机，为以后维护的便利性，要求实现管理机无需密码，直接登录被管理机；
- **安装** ：安装lustre文件系统，包括进行改进的补丁；
- **部署** ：部署lustre文件系统；
- **统一控制** ：采用MULTEXU基础套件进行统一管理控制的工具；
- **测试** ：自动测试(针对Lustre NRS调度)；
- **监测** ：反馈lustre的运行情况；

-------------------

**关于Fdm Lustre QoS**
-----------
高性能并行存储系统（例如数据中心和超级计算机使用的这些系统）中，当大量的client竞争有限的资源（如bandwidth等），性能会急剧下降。这些竞争导致整个存储系统的效率、速度下降。Feedback-driven-Monitor进行Storage traffic Management（存储拥塞管理），提高bandwidth利用率，公平地进行资源分配。

实现方式：基于反馈机制和一定的策略控制拥塞窗口（congestion window）和rate limit来实现client的拥塞控制。具体包括：

-----------

	1. 由于在运行时在client和central coordinator之间仅需要少量通讯协调(只有一个参数Windows Width)，rule-based client Controller可以快速的响应burst I/O。通俗的说就是几乎不需要在任务运行的过程中进行节点间交互、协商来实时调整任务情况;
	
	2. the rule-based client是在自治的，因此系统不会扩展瓶颈;
	
	3. 所有发送到server的I/O请求都可被视作时间序列，该序列会按一个固定的间隔被分为连续的时间段，我们称每个时间段为Time Windows。因此，一个Time Window有一系列I/O请求组成，时间间隔的值成为Time Windows Width;
	
	4. 详细情况参见[设计PPT](https://github.com/ShijunDeng/Feedback-driven-Monitor/blob/master/document/work_reportv20161012A.pptx)

    

-------------------

[DOCUMENT]

# Fdm Lustre QoS TOOL设计

> Fdm Lustre QoS TOOL主要是采用shell script编写的自动化控制套件
## 架构
	├─Fdm-LustreQoS
	│  README.md
	│
	├─batch
	│  ├─authorize
	│  │      distribute.sh
	│  │      execuse.sh
	│  │      nodes_authorize.sh
	│  │      nodes_authorize.sh.origin
	│  │      start_authorize.sh
	│  │
	│  ├─build
	│  │      build_lustre_client.sh
	│  │      build_lustre_server.sh
	│  │      build_newkernel.sh
	│  │      README
	│  │      _patch_metric.sh
	│  │
	│  ├─config
	│  │      hostfile
	│  │      hosts
	│  │      nodes_all.out
	│  │      nodes_authorize.out
	│  │      nodes_client.out
	│  │      nodes_oss.out
	│  │      nodes_server.out
	│  │
	│  ├─config.bake
	│  │      nodes_all.out
	│  │      nodes_authorize.out
	│  │      nodes_client.out
	│  │      nodes_oss.out
	│  │      nodes_server.out
	│  │
	│  ├─ctrl
	│  │      help_doc.txt
	│  │      multexu.sh
	│  │      multexu_lib.sh
	│  │      multexu_ssh.sh
	│  │      __init.sh
	│  │
	│  ├─deploy
	│  │      auto_lustre2.8.0_deploy.sh
	│  │      _configure_ossnode.sh
	│  │      __auto_parted.sh
	│  │      __configure_clientnode.sh
	│  │      __configure_mdsnode.sh
	│  │      __configure_ossnode.sh
	│  │
	│  ├─install
	│  │      auto_lustre2.8.0_install.sh
	│  │      lustre_install_client.sh
	│  │      lustre_install_newkernel.sh
	│  │      lustre_install_pre.sh
	│  │      lustre_install_server.sh
	│  │
	│  ├─lmt
	│  │      lmt_install.sh
	│  │      _cerebro_install.sh
	│  │      _configure_cerebro_conf.sh
	│  │      _configure_mgnode.sh
	│  │      _host_conf.sh
	│  │      _lmt_install.sh
	│  │
	│  ├─test
	│  │  │  auto_test_fio.sh
	│  │  │  clear_var_log_messages.sh
	│  │  │  fio_install.sh
	│  │  │  _test_exe.sh
	│  │  │
	│  │  └─testResult
	│  └─tool
	│          molokai_install.sh
	│          set_display.sh
	│
	├─code
	│      lustre_nrs_sscdt.h
	│      nrs_sscdt.c
	│      README
	│
	├─document
	│      client补丁记录.txt
	│      etc_hosts.xml
	│      history.txt
	│      ltop.txt
	│      ltop_parameters.txt
	│      ref manual.docx
	│
	├─source
	│  ├─build
	│  │  │  lustre_nrs_sscdt.patch
	│  │  │  raid5-mmp-unplug-dev-3.7.patch
	│  │  │  README
	│  │  │
	│  │  └─metric
	│  │          lproc_osc.c
	│  │          lustre_idl.h
	│  │          metric.h
	│  │          obd.h
	│  │          osc_request.c
	│  │          qos_rules.c
	│  │
	│  ├─install
	│  ├─lmt
	│  └─tool
	│
	└─testResult


## 功能说明
	Feedback-driven-Monitor
		├─batch：脚本
		│  ├─authorize：认证
		│  ├─build：编译
		│  ├─configip配置文件
		│  ├─ctrl：MULTEXU工具套件，统一控制
		│  ├─deploy：部署
		│  ├─install：安装
		│  ├─lmt：Lustre Monitoring Tool安装
		│  ├─test：测试
		│  │  └─testResult：测试结果
		│  └─tool：一些常用的工具
		├─code：代码、补丁
		├─source：Feedback-driven-Monitor tool用到的rpm包、资源文件
		│	├─build
		│	├─install
		│	├─lmt
		│	└─tool
		├─document：文档
		└─testResult：测试结果
			
# Fdm-Lustre QoS TOOL使用
>注：根据lustre和Linux kernel的版本，需要适当对工具进行定制和修改，参见源代码中的说明；编译、安装、部署、测试工具中自带的lustre和Linux kernel，除了配置节点IP之外，不需要任何更改

##使用authorize认证
>说明：在一个局域网，在其中指定一台主机做为管理机，其它主机做为被管理机，为以后维护的便利性，要求实现管理机无需密码，直接登录被管理机；假设指定controller作为控制节点，通过shell脚本，实现一次执行，批量配置管理机与被管理机的信任关系，实现管理机免密码登录被管理机。
使用步骤：


    1. 在config文件的nodes_authorize.out中配置好要管理的主机的ip地址，一个ip占据一行，不要包括其它任何无关信息；
    2. 运行 sh start_authorize.sh，根据提示操作
		[root@CentOS1 authorize]# sh ClientAuthorize.sh
		Generating public/private rsa key pair.
		#type Enter directly
		Enter file in which to save the key (/root/.ssh/id_rsa)：
		Created directory '/root/.ssh'.
		#type Enter directly，make empty passward
		Enter passphrase (empty for no passphrase)：
		Enter same passphrase again：
		Your identification has been saved in /root/.ssh/id_rsa.
		Your public key has been saved in /root/.ssh/id_rsa.pub.
		The key fingerprint is：
		6d：bc：5c：f8：32：bf：ee：4a：fe：bf：be：76：8d：29：38：aa root@CentOS1
		The key's randomart image is：
		|                 |
		|                 |
		|                 |
		|         o .     |
		|        S = .    |
		|         o +     |
		|          *..  o.|
		|         oo+. + o| 
		|      E...o***=+ | 
		#the warning occurs because of the option StrictHostKeyChecking=no，just ignore it
		Warning： Permanently added '192.168.10.3' (RSA) to the list of known hosts.
		#Because trust has not yet been established， so still need a password
		root@192.168.122.101's password：
		ServerAuthorize.sh                                                                            100%  664     0.7KB/s   00：00
		Warning： Permanently added '192.168.10.4' (RSA) to the list of known hosts.
		root@192.168.122.102's password：
		ServerAuthorize.sh                                                                            100%  664     0.7KB/s   00：00
		Warning： Permanently added '192.168.10.5' (RSA) to the list of known hosts.
		root@192.168.122.103's password：
		ServerAuthorize.sh                                                                            100%  664     0.7KB/s   00：00
		#Start， after the completion of distribution in each managed machine configuration script execution
		root@192.168.122.101's password：
		root@192.168.122.102's password：
		root@192.168.122.103's password：

##使用build执行自动编译
>说明：build主要对lustre源码、以及Feedback-driven-Monitor的源码进行编译，生成用于安装的rpm包，一般只要在一台机器上编译，生成的rpm可以在其它相同系统的机器上运行
	sh build/build_newkernel.sh
	grep -Ri 'intel' /usr
	rpm -ivh $PKG_PATH/kernel-*.rpm 安装编译生成的包
	/sbin/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --install 2.6.32.431.5.1.el6_lustre
	sh build/build_lustre
	reboot

##使用install安装
>说明：install主要进行安装操作，只需要运行auto_lustre2.8.0_install.sh即可，其它脚本均为自动调用

    sh install/auto_lustre2.8.0_install.sh
	
##使用deploy部署
>说明：自动部署文件系统，用法实例

	sh deploy/auto_lustre2.8.0_deploy.sh --mdsnode=192.168.122.140 --devname=/dev/sda --index=3 

- mdsnode为mdsnode服务器的ip地址
- devname设备名称，将在该设备上格式化进行文件系统安装
- index 分区的index，例如lustre将要挂在到/dev/sda3，则这里的index为3
- 另外，还需要在config文件夹下进行相关的ip地址配置

	nodes_client.out：所有client端的ip地址，一个ip占据一行
	nodes_oss.out：所有oss端的ip地址，一个ip占据一行
	nodes_server.out：oss && mdsnode一起的ip地址，一个ip占据一行

##使用lmt安装Lustre Monitoring Tool
>说明：安装Lustre Monitoring Tool，用法实例

	sh lmt/lmt_install.sh --mdsnode=192.168.122.140 --lmt_mgnode=192.168.122.141

- mdsnode为mdsnode服务器的ip地址
- lmt_mgnode为lmt管理节点ip地址,缺省情况下为当前节点
- 参见[lmt配置](https://github.com/ShijunDeng/Feedback-driven-Monitor/blob/master/document/lmt.docx)配置相应的/etc/hosts、/etc/hostfile、/etc/cerebro.conf文件后才能正常使用该命令

##使用test测试
>说明：进行测试，可以根据需要修改auto_test_fio.sh中的参数配置，详细见auto_test_fio.sh中的注释

	 sh test/auto_test_fio.sh --random="-rwmixread=50"
- random参数指定针对random读写方式的一些特殊添加命令,只对random读写方式生效,实例中指定了读写的控制比例

##使用tool
>说明：tool中集成一些常见的工具类脚本,使用说明
	 
	sh test/set_display.sh 1440 900
- 设置分辨率为1440*900



##使用MULTEXU进行统一控制
>说明：为便于测试过程中的管理中的管理，使用MULTEXU进行统一控制，具体使用方法见 [MULTEXU](https://github.com/ShijunDeng/multexu)

>另外, 参见 [history.txt](https://github.com/ShijunDeng/Feedback-driven-Monitor/blob/master/document/history.txt) 中常见的控制命令

## 反馈与建议
- QQ：946057490
- 邮箱：<dengshijun1992@gmail.com> <SjDeng@hust.edu.cn>

---------
感谢阅读这份帮助文档。