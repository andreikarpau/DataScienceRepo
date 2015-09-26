import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * a bolt that finds the top n words.
 */
public class TopNFinderBolt extends BaseBasicBolt {
	private Map<String, Integer> currentTopWords = new HashMap<String, Integer>();
	private int N;

	private long intervalToReport = 20;
	private long lastReportTime = System.currentTimeMillis();

	public TopNFinderBolt(int N) {
		this.N = N;
	}

	@Override
	public void execute(Tuple tuple, BasicOutputCollector collector) {

		String word = tuple.getStringByField("word");
		Integer count = tuple.getIntegerByField("count");
		currentTopWords.put(word, count);
		currentTopWords = MapUtil.sortByValue(currentTopWords);

		int size = currentTopWords.size();
		if (N < size)
			currentTopWords.remove(currentTopWords.keySet().toArray()[size - 1]);

		// reports the top N words periodically
		if (System.currentTimeMillis() - lastReportTime >= intervalToReport) {
			collector.emit(new Values(printMap()));
			lastReportTime = System.currentTimeMillis();
		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {

		declarer.declare(new Fields("top-N"));

	}

	public String printMap() {
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.append("top-words = [ ");
		for (String word : currentTopWords.keySet()) {
			stringBuilder.append("(" + word + " , " + currentTopWords.get(word)
					+ ") , ");
		}
		int lastCommaIndex = stringBuilder.lastIndexOf(",");
		stringBuilder.deleteCharAt(lastCommaIndex + 1);
		stringBuilder.deleteCharAt(lastCommaIndex);
		stringBuilder.append("]");
		return stringBuilder.toString();

	}

	public static class MapUtil {
		public static <K extends Comparable<? super K>, V extends Comparable<? super V>> Map<K, V> sortByValue(
				Map<K, V> map) {
			List<Map.Entry<K, V>> list = new LinkedList<Map.Entry<K, V>>(
					map.entrySet());
			Collections.sort(list, new Comparator<Map.Entry<K, V>>() {
				public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
					if ((o2.getValue()).compareTo(o1.getValue()) != 0) {
						return (o2.getValue()).compareTo(o1.getValue());
					} else {
						return (o1.getKey()).compareTo(o2.getKey());
					}
				}
			});

			Map<K, V> result = new LinkedHashMap<K, V>();

			for (Map.Entry<K, V> entry : list) {
				result.put(entry.getKey(), entry.getValue());
			}

			return result;
		}
	}
}
