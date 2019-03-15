#!/usr/bin/env python3
import os
import argparse
import time
import subprocess
import paramiko

is_run_flink=True
is_run_ts=True
is_run_oai = True
epc_cmd=""
enb_cmd=""
kafka_cmd=""
cmd = "ls"
oai_password="password"

ssh_flink = "user@192.168.200.1"
ssh_ts = "user@192.168.200.2"
ssh_oai = "user@192.168.200.3"

args=""
kafka_conf=""
is_kill_all_oai = False
is_run_all_oai = True

def exe_cmd(cmd):
    try:
        print("shell: ", cmd)    
        subprocess.call(cmd, shell=True)
        
    except:    
        print("errno_num")

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

def run_mme():
    cmd = 'xterm  -T "mme" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_mme" &'
    exe_cmd(cmd)

def run_hss():
    cmd = 'xterm  -T "hss" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_hss" &'
    exe_cmd(cmd)



def run_spgw():
    cmd = 'xterm  -T "spgw" -e ssh ' + ssh_oai + ' "/home/user/openair-cn/scripts/run_spgw" &'
    exe_cmd(cmd)


def run_epc():
    cmd = "ssh user@192.168.200.3 'source /home/user/openair-cn/oaienv'"
    exe_cmd(cmd)
    time.sleep(1)
    
    run_hss()
    time.sleep(2)
    run_mme()
    time.sleep(2)
    run_spgw()
    time.sleep(2)

def run_enb():
    cmd ='xterm -T "enb" -e ssh '+ ssh_oai +' " source /home/user/openairinterface5g/oaienv; sudo -E ~/openairinterface5g/cmake_targets/lte_build_oai/build/lte-softmodem -O ~/openairinterface5g/conf/enb.band7.tm1.25PRB.usrpb210.conf" &' 
    exe_cmd(cmd)


def run_zookeeper():        
    cmd = "xterm  -T \"zookeeper\" -hold -e "
    cmd += args.kafkaDir + "/bin/zookeeper-server-start.sh "
    cmd += args.kafkaDir + "/config/zookeeper.properties &"
    exe_cmd(cmd)

def run_brokers():
    cmd = "xterm  -T \"broker\"  -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-server-start.sh "
    cmd += args.kafkaDir + "/config/server.properties &"
    exe_cmd(cmd)

def run_producer():        
    cmd = "xterm -T \"producer\" -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic "+ args.kafkaTopic +"&"
    exe_cmd(cmd)

def run_consumer():
    cmd = "xterm  -T \"consumer\"  -hold -e "
    cmd += args.kafkaDir + "/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic "+ args.kafkaTopic +"&"
    exe_cmd(cmd)

def run_flink_app():
    pass

def run_ts():
    pass

def run_ws():
    pass

def kill_pid(pid):
    cmd ='ssh user@192.168.200.3 sudo kill '+pid
    exe_cmd(cmd)

def get_pids(grep_item):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #handle no known_hosts error
    ssh.connect('192.168.200.3', username='user', password=oai_password)
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep "+grep_item+" | grep -v grep | awk '{print $2}'")
    #stdin.write('mme pids:\n')
    stdin.flush()
    stdout=stdout.readlines()
    ssh.close()
    pids=[]
    for p in stdout:
        pids.append(p[:-1]) #remove last char, which is \n

    return pids

    

def kill_mme():
    print("killing mme..")
    for pid in get_pids("mme"):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_spgw():
    print("killing spgw..")
    for pid in get_pids("spgw"):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_hss():
    print("killing hss..")
    for pid in get_pids("hss"):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_epc():
    kill_mme()
    kill_spgw()
    kill_hss()

def kill_enb():
    print("killing enb..")
    for pid in get_pids("lte-softmodem"):
        cmd = 'ssh ' + ssh_oai + ' "sudo kill ' + pid + '"'
        exe_cmd(cmd)

def kill_oai():
    kill_epc()
    kill_enb()

def run_oai():
    run_epc()
    run_enb()

    #run_zookeeper()
    #run_brokers()

def main(args):

    if args.kill_all_oai == "true" or args.kill_all_oai == "t":
        kill_oai()
    else:
        run_oai()

    """
    if args.runZookeeper==None or args.runZookeeper=="true":
        run_zookeeper()    
        time.sleep(1)

    if args.runBrokers==None or args.runBrokers=="true":
        run_brokers()    
        time.sleep(1)

    if args.runProduer != None or args.runBrokers=="true":
        run_producer()    
        time.sleep(1)

    if args.runConsumer != None or args.runBrokers=="true":
        run_consumer()    
        time.sleep(1)
    """

    if is_run_flink:
        pass
    
    if is_run_ts:
        pass


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
    parser.add_argument("--kill_all_oai","-kao",help="kill all aoi: epc and enb: -kao t or -kao true")
    parser.add_argument("--run_all_oai","-rao",help="run all aoi: epc and enb")

    args = parser.parse_args()


    if args.kafkaDir==None:
        args.kafkaDir = "~/app/kafka_2.11-2.1.0"
    
    if args.kafkaTopic==None:
        args.kafkaTopic = "oai"

    if args.spgwNic == None:
        args.spgwNic = "wlp2s0"
    
    
    main(args)