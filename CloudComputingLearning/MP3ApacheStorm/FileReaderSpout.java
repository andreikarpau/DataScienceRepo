import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Map;

import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.IRichSpout;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;
import backtype.storm.utils.Utils;

public class FileReaderSpout implements IRichSpout {
	private SpoutOutputCollector _collector;
	private TopologyContext context;
	BufferedReader reader = null;

	@Override
	public void open(Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		this.context = context;
		this._collector = collector;

		try {
			String fileName = conf.get("inputFileName").toString();
			reader = new BufferedReader(new FileReader(fileName));
		} catch (Exception e) {

		}
	}

	@Override
	public void nextTuple() {
		try {
			String nextLine = reader.readLine();

			if (nextLine != null) {
				_collector.emit(new Values(nextLine));
			} else {
				Thread.sleep(5000);
			}
		} catch (Exception e) {

		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {

		declarer.declare(new Fields("word"));

	}

	@Override
	public void close() {
		try {
			reader.close();
		} catch (Exception e) {

		}
	}

	@Override
	public void activate() {
	}

	@Override
	public void deactivate() {
	}

	@Override
	public void ack(Object msgId) {
	}

	@Override
	public void fail(Object msgId) {
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}
