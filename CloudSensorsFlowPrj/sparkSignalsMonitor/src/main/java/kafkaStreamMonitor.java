/**
 * Created by askofen on 30.03.16.
 */

import kafka.serializer.StringDecoder;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.streaming.Duration;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaPairInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka.KafkaUtils;
import scala.Tuple2;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class kafkaStreamMonitor {
    private static int bottomAlarmBorder = -100;
    private static int topAlarmBorder = 100;

    public static void main(String[] args) throws IOException {
        if (args.length < 3) {
            System.exit(1);
        }

        String className = kafkaStreamMonitor.class.getSimpleName();
        SparkConf sparkConf = new SparkConf().setAppName(className);

        Map<String, String> paramsMap = new HashMap<String, String>();
        Map<String, Integer> topicMap = new HashMap<String, Integer>();

        fillBaseStreamingParams(args, paramsMap, sparkConf, topicMap);
        JavaStreamingContext jssc = new JavaStreamingContext(sparkConf, new Duration(5000));
        JavaPairInputDStream<String, String> messages = KafkaUtils.createDirectStream(jssc, String.class, String.class, StringDecoder.class, StringDecoder.class, paramsMap, topicMap.keySet());

        JavaDStream<String> lines = messages.map(getBaseInputPreprocessingFunction());
        JavaDStream<String> alarmLines = lines.filter(new Function<String, Boolean>() {
            public Boolean call(String input) throws Exception {
                String[] values = input.split(" ");

                if (values.length < 3)
                {
                    return false;
                }

                int sensorValue = Integer.parseInt(values[2]);

                if (sensorValue < bottomAlarmBorder || topAlarmBorder < sensorValue)
                {
                    return true;
                }

                return false;
            }
        });

        alarmLines.foreach(new Function<JavaRDD<String>, Void>() {
            public Void call(JavaRDD<String> v1) throws Exception {
                List<String> elements = v1.collect();

//                HBaseConfiguration hConf = new HBaseConfiguration();
//                HTable hTable = new HTable(hConf, "test");
//                Put thePut = new Put(Bytes.toBytes(i));
//                thePut.add(Bytes.toBytes("cf"), Bytes.toBytes("a"), Bytes.toBytes(record));
//                hTable.put(thePut);

                return null;
            }
        });
        alarmLines.print();

        jssc.start();
        jssc.awaitTermination();
    }

    public static void fillBaseStreamingParams(String[] args, Map<String, String> paramsMap, SparkConf sparkConf, Map<String, Integer> topicMap) throws IOException{
        paramsMap.put("zookeeper.connect", args[0]);
        paramsMap.put("metadata.broker.list", args[0].split(":")[0] + ":6667");
        paramsMap.put("group.id", args[1]);

        paramsMap.put("zookeeper.connection.timeout.ms", "5000");
        sparkConf.set("spark.streaming.kafka.maxRatePerPartition", "100000");

        for (String argument: args){
            if (argument.contains("--fromStart")){
                paramsMap.put("auto.offset.reset", "smallest");
            }
            if (argument.contains("--minValue")){
                String[] strings = argument.split(":");
                bottomAlarmBorder = Integer.parseInt(strings[1]);
            }
            if (argument.contains("--maxValue")){
                String[] strings = argument.split(":");
                topAlarmBorder = Integer.parseInt(strings[1]);
            }
        }

        int numThreads = 2;
        String topicName = args[2];

        topicMap.put(topicName, numThreads);
    }

    public static Function<Tuple2<String, String>, String> getBaseInputPreprocessingFunction(){
        return new Function<Tuple2<String, String>, String>() {
            private static final long serialVersionUID = 1L;

            public String call(Tuple2<String, String> arg0) throws Exception {
                return arg0._2();
            }
        };
    }
}
