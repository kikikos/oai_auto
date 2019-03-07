dir=/home/yuchia/app/kafka_2.11-2.1.0; 

xterm -hold -e "$dir/bin/zookeeper-server-start.sh  $dir/config/zookeeper.properties" &
sleep 3
xterm -hold -e "$dir/bin/kafka-server-start.sh $dir/config/server.properties" &
sleep 3
#xterm -hold -e "$dir/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic oai-ts" &
#xterm -hold -e "$dir/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic oai"
