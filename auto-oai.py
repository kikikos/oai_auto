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
"""
def run_kafka(args):
    cmd_zk = "xterm -hold -e "
    cmd_zk += args.kafkaDir + "/bin/zookeeper-server-start.sh "
    cmd_zk += args.kafkaDir + "/config/zookeeper.properties &"    
    
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
"""

def run_zookeeper(args):        
    cmd = "xterm -hold -e "
    cmd += args.kafkaDir + "/bin/zookeeper-server-start.sh "
    cmd += args.kafkaDir + "/config/zookeeper.properties &"
    exe_cmd(cmd)

def run_brokers(args):
    cmd = "xterm -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-server-start.sh "
    cmd += args.kafkaDir + "/config/server.properties &"
    exe_cmd(cmd)

def run_producer(args):        
    cmd = "xterm -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic "+ args.kafkaTopic +"&"
    exe_cmd(cmd)

def run_consumer(args):
    cmd = "xterm -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic "+ args.kafkaTopic +"&"
    exe_cmd(cmd)

def main(args):
    if args.runZookeeper==None or args.runZookeeper=="true":
        run_zookeeper(args)    
        time.sleep(1)

    if args.runBrokers==None or args.runBrokers=="true":
        run_brokers(args)    
        time.sleep(1)

    if args.runProduer != None or args.runBrokers=="true":
        run_producer(args)    
        time.sleep(1)

    if args.runConsumer != None or args.runBrokers=="true":
        run_consumer(args)    
        time.sleep(1)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafkaDir","-dir",help="root directory of Kafka")
    parser.add_argument("--runZookeeper","-zookeeper",help="run zookeeper")
    parser.add_argument("--runBrokers","-brokers", help="run brokers")
    parser.add_argument("--runProduer","-produer",help="run producer")
    parser.add_argument("--runConsumer","-consumer",help="run consumer")
    parser.add_argument("--kafkaTopic","-topic",help="Kafka topic")
    parser.add_argument("--spgwNic","-nic",help="network interface for spgw")
    parser.add_argument("--enb","-e",help="enb autorun")
    args = parser.parse_args()

    if args.kafkaDir==None:
        args.kafkaDir = "~/app/kafka_2.11-2.1.0"
    
    if args.kafkaTopic==None:
        args.kafkaTopic = "oai"

    if args.spgwNic == None:
        args.spgwNic = "wlp2s0"
    main(args)