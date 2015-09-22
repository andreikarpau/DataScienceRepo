
import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

/**
 * This topology counts the words from sentences emmited from a random sentence spout.
 */
public class TopWordFinderTopologyPartA {

  public static void main(String[] args) throws Exception {

    TopologyBuilder builder = new TopologyBuilder();

    Config config = new Config();
    config.setDebug(true);

    builder.setSpout("spout", new RandomSentenceSpout(), 5);
    builder.setBolt("split", new SplitSentenceBolt(), 8).shuffleGrouping("spout");
    builder.setBolt("count", new WordCountBolt(), 12).fieldsGrouping("split", new Fields("word")); 
   
    config.setMaxTaskParallelism(3);

    LocalCluster cluster = new LocalCluster();
    cluster.submitTopology("word-count", config, builder.createTopology());

    //wait for 60 seconds and then kill the topology
    Thread.sleep(60 * 1000);

    cluster.shutdown();
  }
}
