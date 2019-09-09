FROM centos:7

RUN yum -y update && yum -y install git gcc-c++ python2.7 python-devel.x86_64 sudo ssh epel-release
RUN yum -y install python-pip && pip install --upgrade pip
RUN yum -y clean all

RUN pip install lmdb psutil
#pip install -r requirements.txt
#pip install -r requirements-homebase.txt
#pip: scipy

COPY lmdb_test4.py /lmdb_tests/
RUN chmod a+x /lmdb_tests/lmdb_test4.py

#CMD  ["/usr/bin/python"]
CMD  ["/bin/bash"]

#docker build --force-rm --tag lmdb_shared_mem:v0.1 .
#docker run --rm --interactive --tty lmdb_shared_mem:v0.1
