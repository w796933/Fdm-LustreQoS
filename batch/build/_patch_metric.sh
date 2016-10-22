#!/bin/bash
# POSIX
#
#description:    add and patch files for metric
#     author:    ShijunDeng
#      email:    dengshijun1992@gmail.com
#       time:    2016-10-12
#

#lustre/
cp -rf ${MULTEXU_SOURCE_DIR}/build/metric/metric-tests lustre/
#lustre/osc/
cp ${MULTEXU_SOURCE_DIR}/build/metric/qos_rules.c lustre/osc/
#lustre/osc/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/osc_request.c lustre/osc/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/lproc_osc.c lustre/osc/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/osc_cache.c lustre/osc/
#lustre/include/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/obd.h lustre/include/
#lustre/include/lustre/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/lustre_idl.h lustre/include/lustre/
#lustre/ptlrpc/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/pack_generic.c lustre/ptlrpc/
#lustre/obdclass/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/genops.c lustre/obdclass/
yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/lprocfs_status.c lustre/obdclass/

#yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/wiretest.c lustre/utils/
#有错误 lustre/utils/wiretest.c lustre/ptlrpc/wiretest.c两个文件名称相同，内容略有出入，因此修改为使用补丁修改，精确修改
#yes | cp ${MULTEXU_SOURCE_DIR}/build/metric/wiretest.c lustre/ptlrpc/

cp ${MULTEXU_SOURCE_DIR}/build/metric/metric.h lustre/include/
