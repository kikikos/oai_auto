cd /home/user/app/kafka_2.11-2.1.0; 

xterm -hold -e "bin/zookeeper-server-start.sh  config/zookeeper.properties" &
sleep 3
xterm -hold -e "bin/kafka-server-start.sh config/server.properties" &
sleep 3
xterm -hold -e "bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic oai" &
xterm -hold -e "bin/kafka-console-producer.sh --broker-list localhost:9092 --topic oai"