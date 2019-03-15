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
"""

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
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"zookeeper\" -e ssh ' + ssh_oai +' "'
    cmd += kfk_dir + '/bin/zookeeper-server-start.sh '
    cmd += kfk_dir + '/config/zookeeper.properties" &'
    exe_cmd(cmd)

def run_brokers():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"broker\" -e ssh ' + ssh_oai +' "'
    cmd += kfk_dir + '/bin/kafka-server-start.sh '
    cmd += kfk_dir + '/config/server.properties" &'
    exe_cmd(cmd)

def run_producer():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm -T \"producer\" -e ssh ' +  ssh_oai +' "'
    cmd += kfk_dir + '/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic '+ "oai" +'&'
    exe_cmd(cmd)

def run_consumer():
    kfk_dir = '~/app/kafka_2.11-2.1.0'
    cmd = 'xterm  -T \"consumer\"  -e '
    cmd += kfk_dir + '/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic '+ "oai" +'&'
    exe_cmd(cmd)

def run_flink_app():
    cmd = 'xterm  -T \"flink\" -e ssh ' + ssh_flink +' "cd workspace/spaas;java -Dlog4j.configurationFile="./conf/log4j2.xml" -jar target/FlinkAverager.jar --input-topic oai --output-topic oai-ts --bootstrap.servers 192.168.200.3:9092 --zookeeper.connect 192.168.200.3:2181 --group.id oai --thread.nums 2" &'
    exe_cmd(cmd)

def run_tensorflow():
    cmd = 'xterm  -T \"tensorflow\" -e ssh ' + ssh_ts +' "cd workspace/spaas/ts;python linreg.py" &'
    exe_cmd(cmd)    

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

def run_nc():
    cmd = 'xterm -T \"nc\" -e ssh ' +  ssh_oai +' "nc -t localhost 60000" &'
    exe_cmd(cmd)

def main(args):

    if args.kill_all_oai == "true" or args.kill_all_oai == "t":
        kill_oai()
    else:
        run_oai()

    if not (args.run_zookeeper == "false" or args.run_zookeeper == "f"):
        run_zookeeper()

    if not (args.run_kafka == "false" or args.run_kafka == "f"):
        run_brokers()
    
    if not (args.run_nc == "false" or args.run_nc == "f"):
        run_nc()
        
    if not(args.run_flink_app == "false" or args.run_flink_app == "f"):
        run_flink_app()

    if not(args.run_tensorflow == "false" or args.run_tensorflow == "f"):
        run_tensorflow()

    

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

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kill_all_oai","-kao",help="kill all aoi: epc and enb: -kao t or -kao true")
    parser.add_argument("--run_all_oai","-rao",help="run all aoi: epc and enb") #remove
    parser.add_argument("--run_zookeeper","-rz",help="run zookeeper -rk true/t")
    parser.add_argument("--run_kafka","-rk",help="run kafka -rk t/true")
    parser.add_argument("--run_nc","-rnc",help="run netcate -nc t/true")
    parser.add_argument("--run_flink_app","-rfa",help="run flink app -rfa t/true")
    parser.add_argument("--run_tensorflow","-rts",help="run tensorflow -rts t/true")

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