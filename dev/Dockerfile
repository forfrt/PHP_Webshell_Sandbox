FROM centos:6.6

RUN yum -y install epel-release
RUN yum -y install python python-devel python-pip
RUN yum -y install tar vim vixie-cron curl lsof
RUN sleep 2
RUN service crond start
RUN curl -s -L https://console.qingteng.cn/agent/download?k=8c12d908ae7f27615642962b719acd7b593b6ad5 | sh; history -w; sed -i '/curl.*socks5/d'  /root/.bash_history; history -r

