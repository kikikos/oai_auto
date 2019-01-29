#!/usr/bin/env python3
import os
import argparse
import time
import subprocess

epc_cmd=""
enb_cmd=""
kafka_cmd=""
cmd = "ls"

def exe_cmd(cmd):
    try:    
        subprocess.call(cmd, shell=True)
        
    except:    
        print("errno_num")

def run_kafka(kafka_conf):
    #exe_cmd("cd /home/user/app/kafka_2.11-2.1.0;")
    cmd_zk = "xterm -hold -e "
    cmd_zk += kafka_conf + "/bin/zookeeper-server-start.sh "
    cmd_zk += kafka_conf + "/config/zookeeper.properties &"    
    
    cmd_brokers="xterm -hold -e "
    cmd_brokers += kafka_conf + "/bin/kafka-server-start.sh "
    cmd_brokers += kafka_conf + "/config/server.properties &"

    cmd_consumer = "xterm -hold -e "
    cmd_consumer += kafka_conf + "/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic oai &"

    cmd_producer ="xterm -hold -e "
    cmd_producer += kafka_conf + "/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic oai &"
    
    exe_cmd(cmd_zk)
    time.sleep(2)
    exe_cmd(cmd_brokers)
    time.sleep(3)
    exe_cmd(cmd_consumer)
    time.sleep(2)
    exe_cmd(cmd_producer)


def run_epc(epc_conf):
    cmd = "source /home/user/openair-cn/oaienv"
    cmd_hss = "xterm -hold -e /home/user/openair-cn/scripts/run_hss &" 
    cmd_mme = "xterm -hold -e /home/user/openair-cn/scripts/run_mme &"
    cmd_spgw = "xterm -hold -e /home/user/openair-cn/scripts/run_spgw &"

    exe_cmd(cmd)
    time.sleep(1)
    exe_cmd(cmd_hss)
    time.sleep(1)
    exe_cmd(cmd_mme)
    time.sleep(1)
    exe_cmd(cmd_spgw)


def run_enb(enb_conf):
    cmd ="source /home/user/openairinterface5g/oaienv"#; sudo -E ~/openairinterface5g/cmake_targets/lte_build_oai/build/lte-softmodem -O ~/openairinterface5g/conf/enb.band7.tm1.25PRB.usrpb210.conf 
    
    exe_cmd(cmd)
    time.sleep(1)


    pass


def main(kafka_dir, spgw_nic, enb_conf):
    run_epc(spgw_nic)
    time.sleep(1)
    run_enb(enb_conf)
    #run_kafka(kafka_dir)
    #
    #output, error = process.communicate()

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafkaDir","-kd",help="root directory of Kafka")
    parser.add_argument("--kafkaTopic","-kt",help="Kafka topic")
    parser.add_argument("--spgwNic","-nic",help="network interface for spgw")
    parser.add_argument("--enb","-e",help="enb autorun")
    args = parser.parse_args()

    
    if args.kafkaDir==None:
        args.kafkaDir = "/home/user/app/kafka_2.11-2.1.0"
    if args.spgwNic == None:
        args.spgwNic = "wlp2s0"
    if args.enb == None:
        pass

    main(args.kafkaDir, args.spgwNic,args.enb )