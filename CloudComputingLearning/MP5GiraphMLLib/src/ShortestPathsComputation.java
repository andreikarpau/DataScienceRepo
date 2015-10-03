import org.apache.giraph.conf.LongConfOption;
import org.apache.giraph.edge.Edge;
import org.apache.giraph.graph.BasicComputation;
import org.apache.giraph.graph.Vertex;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;

import java.io.IOException;

/**
 * Compute shortest paths from a given source.
 */
public class ShortestPathsComputation extends
		BasicComputation<IntWritable, IntWritable, NullWritable, IntWritable> {
	/** The shortest paths id */
	public static final LongConfOption SOURCE_ID = new LongConfOption(
			"SimpleShortestPathsVertex.sourceId", 1, "The shortest paths id");

	/**
	 * Is this vertex the source id?
	 *
	 * @param vertex
	 *            Vertex
	 * @return True if the source id
	 */
	private boolean isSource(Vertex<IntWritable, ?, ?> vertex) {
		return vertex.getId().get() == SOURCE_ID.get(getConf());
	}

	@Override
	public void compute(Vertex<IntWritable, IntWritable, NullWritable> vertex,
			Iterable<IntWritable> messages) throws IOException {


		if (getSuperstep() == 0) {
			if (!isSource(vertex)) {
				vertex.setValue(new IntWritable(Integer.MAX_VALUE));
				vertex.voteToHalt();
				return;
			}

			vertex.setValue(new IntWritable(0));

			for (Edge<IntWritable, NullWritable> edge : vertex.getEdges()) {
				IntWritable neighbor = edge.getTargetVertexId();
				sendMessage(neighbor, new IntWritable(1));
			}

			vertex.voteToHalt();
			return;
		}

		int minDist = vertex.getValue().get();
		boolean changed = false;
		// did we get a smaller id ?
		for (IntWritable message : messages) {
			int newDist = message.get();
			if (newDist < minDist) {
				minDist = newDist;
				changed = true;
			}
		}

		// propagate new component id to the neighbors
		if (changed) {
			vertex.setValue(new IntWritable(minDist));
			sendMessageToAllEdges(vertex, new IntWritable(minDist + 1));
		}
		vertex.voteToHalt();

	}
}
