FROM centos:6.6

RUN rpm -Uvh http://repo.webtatic.com/yum/el6/latest.rpm  
RUN yum -y install epel-release
RUN yum -y install php54w php54w-common php54w-cli php54w-fpm php54w-devel
RUN yum -y install python python-devel python-pip
RUN pip install flask-restful

ADD php.ini /etc/php.ini
ADD libwebshell.so /usr/lib64/php/modules/

RUN mkdir       /home/Projects/
ADD DB_Init.py  /home/Projects/
ADD sandbox.py  /home/Projects/
WORKDIR         /home/Projects/

RUN python DB_Init.py
CMD python sandbox.py
