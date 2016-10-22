#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# description: 根据lmt工具中监测的数据计算一些有用的指标例如bandwidth等等
#      author: ShijunDeng
#       email: dengshijun1992@gmail.com
#        time: 2016-10-14
# *
from entity import hostnode
from entity import ltop_mdt, ltop_ost
from utils import get_oss_node_list, get_ltop_list


#
# ost的node节点和对应的lmt中ltop命令的信息
#
class ost_hostnode_ltop:
    def __init__(self):
        self.hostnode_var = None
        self.ltop_ost_list = []

    #
    # 判断该条信息是否属于该hostnode
    #
    def __accept__(self, ltop_ost_var):
        return ltop_ost_var.node == self.hostnode_var.hostname

    #
    # 从ltop_ost_list_other中筛选出属于当前节点的ltop信息并添加到当前的ltop_ost_list中
    #
    def filter_add_ltop_ost_list(self, ltop_ost_list_other):
        for ltop_ost_var in ltop_ost_list_other:
            if self.__accept__(ltop_ost_var):
                self.ltop_ost_list.append(ltop_ost_var)

    #
    # 直接添加到当前hostnode的ltop_ost_list,不做判断
    #
    def add_ltop_host(self, ltop_ost_var):
        self.ltop_ost_list.append(ltop_ost_var)

    #
    # 添加的时候同时判断是否属于当前的hostnode,属于当前的hostnode才添加
    #
    def filter_add_ltop_ost(self, ltop_ost_var):
        if not ltop_ost_var and self.__accept__(ltop_ost_var):
            self.add_ltop_host(ltop_ost_var)

    def sort_ltop_ost_list(self, sort_key):
        sorted(self.ltop_ost_list, sort_key, reverse=False)


def cal_detail():
    mds_list = get_oss_node_list()
    ost_hostnode_ltop_list = []
    ltop_data_list = get_ltop_list()
    ltop_ost_list = ltop_data_list['ostlist']
    ltop_mdt_list = ltop_data_list['mdtlist']
    for element in mds_list:
        ost_hostnode_ltop_var = ost_hostnode_ltop()
        ost_hostnode_ltop_var.hostnode_var = element

        ost_hostnode_ltop_var.filter_add_ltop_ost_list(ltop_ost_list)
        sorted(ost_hostnode_ltop_var.ltop_ost_list, key=lambda top_ost_var: top_ost_var.trcv, reverse=False)
        # ost_hostnode_ltop_var.sort_ltop_ost_list(lambda top_ost_var: top_ost_var.trcv)
        ost_hostnode_ltop_list.append(ost_hostnode_ltop_var)
        print("---------------%s---------------------" % element.hostname)
        i = 1
        while i < len(ost_hostnode_ltop_var.ltop_ost_list):
            br = (ost_hostnode_ltop_var.ltop_ost_list[i].read_bytes - ost_hostnode_ltop_var.ltop_ost_list[
                i - 1].read_bytes) / (
                     ost_hostnode_ltop_var.ltop_ost_list[i].trcv - ost_hostnode_ltop_var.ltop_ost_list[i - 1].trcv) / (
                     1024 * 1024)
            bw = (ost_hostnode_ltop_var.ltop_ost_list[i].write_bytes - ost_hostnode_ltop_var.ltop_ost_list[
                i - 1].write_bytes) / (
                     ost_hostnode_ltop_var.ltop_ost_list[i].trcv - ost_hostnode_ltop_var.ltop_ost_list[i - 1].trcv) / (
                     1024 * 1024)
            print("br=%f,bw=%f,filesfree=%d -> %d,filestotal=%d -> %d,sfree=%f -> %f,stotal=%f -> %f" % (
            br, bw, ost_hostnode_ltop_var.ltop_ost_list[i - 1].filesfree,
            ost_hostnode_ltop_var.ltop_ost_list[i].filesfree
            , ost_hostnode_ltop_var.ltop_ost_list[i - 1].filestotal, ost_hostnode_ltop_var.ltop_ost_list[i].filestotal,
            ost_hostnode_ltop_var.ltop_ost_list[
                i - 1].kbytesfree / (1024 * 1024), ost_hostnode_ltop_var.ltop_ost_list[
                i].kbytesfree / (1024 * 1024), ost_hostnode_ltop_var.ltop_ost_list[
                i - 1].kbytestotal / (1024 * 1024), ost_hostnode_ltop_var.ltop_ost_list[
                i].kbytestotal / (1024 * 1024)))
            i += 1
