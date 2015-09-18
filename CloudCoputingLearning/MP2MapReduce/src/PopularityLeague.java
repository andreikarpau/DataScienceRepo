import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class PopularityLeague extends Configured implements Tool {

	public static void main(String[] args) throws Exception {
		int res = ToolRunner.run(new Configuration(), new PopularityLeague(), args);
		System.exit(res);
	}

	
	@Override
	public int run(String[] args) throws Exception {
		Configuration conf = this.getConf();
		FileSystem fs = FileSystem.get(conf);
		Path tmpPath = new Path("/mp2/tmp");
		fs.delete(tmpPath, true);

		Job jobA = Job.getInstance(conf, "Link count");

		jobA.setOutputKeyClass(LongWritable.class);
		jobA.setOutputValueClass(LongWritable.class);
		jobA.setMapOutputKeyClass(IntWritable.class);
		jobA.setMapOutputValueClass(IntWritable.class);

		jobA.setMapperClass(LinkCountMap.class);
		jobA.setReducerClass(LinkCountReduce.class);

		FileInputFormat.setInputPaths(jobA, new Path(args[0]));
		FileOutputFormat.setOutputPath(jobA, tmpPath);

		jobA.setJarByClass(PopularityLeague.class);
		jobA.waitForCompletion(true);

		Job jobB = Job.getInstance(conf, "Popularity League");
		jobB.setOutputKeyClass(IntWritable.class);
		jobB.setOutputValueClass(IntWritable.class);

		jobB.setMapOutputKeyClass(NullWritable.class);
		jobB.setMapOutputValueClass(IntArrayWritable.class);

		jobB.setMapperClass(PopularityLeagueMap.class);
		jobB.setReducerClass(PopularityLeagueReduce.class);
		jobB.setNumReduceTasks(1);

		FileInputFormat.setInputPaths(jobB, tmpPath);
		FileOutputFormat.setOutputPath(jobB, new Path(args[1]));

		jobB.setJarByClass(PopularityLeague.class);
		return jobB.waitForCompletion(true) ? 0 : 1;
	}

	public static class IntArrayWritable extends ArrayWritable {
		public IntArrayWritable() {
			super(IntWritable.class);
		}

		public IntArrayWritable(Integer[] numbers) {
			super(IntWritable.class);
			IntWritable[] ints = new IntWritable[numbers.length];
			for (int i = 0; i < numbers.length; i++) {
				ints[i] = new IntWritable(numbers[i]);
			}
			set(ints);
		}
	}

	public static String readHDFSFile(String path, Configuration conf) throws IOException{
		Path pt=new Path(path);
		FileSystem fs = FileSystem.get(pt.toUri(), conf);
		FSDataInputStream file = fs.open(pt);
		BufferedReader buffIn=new BufferedReader(new InputStreamReader(file));

		StringBuilder everything = new StringBuilder();
		String line;
		while( (line = buffIn.readLine()) != null) {
			everything.append(line);
			everything.append("\n");
		}
		return everything.toString();
	}

	public static class LinkCountMap extends Mapper<Object, Text, IntWritable, IntWritable> {
		@Override
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line, ": ");           
                        
            Boolean firstPageHandled = false;
            
            while (tokenizer.hasMoreTokens()) {
                String pageNum = tokenizer.nextToken().trim().toLowerCase();
                
                if (pageNum == null || pageNum.isEmpty()){
                	continue;
                }

                int outKey = Integer.parseInt(pageNum);
                int numLinks = 1;
                
                if (firstPageHandled){              	
                }else{
                	numLinks = 0;
                	firstPageHandled = true;
                }
                
                context.write(new IntWritable(outKey), new IntWritable(numLinks));               
            }
		}
	}

	public static class LinkCountReduce extends Reducer<IntWritable, IntWritable, LongWritable, LongWritable> {
		@Override
		public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
			Integer sum = 0;

			for (IntWritable val: values) {
				sum += val.get();
			}

			context.write(new LongWritable(key.get()), new LongWritable(sum));   
		}
	}

	public static class PopularityLeagueMap extends Mapper<LongWritable, Text, NullWritable, IntArrayWritable> {
		ArrayList<Integer> leagues;

		@Override
		protected void setup(Context context) throws IOException,InterruptedException {
			Configuration conf = context.getConfiguration();
			String leaguePath = conf.get("league");
			List<String> leaguesStrs = Arrays.asList(readHDFSFile(leaguePath, conf).split("\n"));
			this.leagues = new ArrayList<Integer>();

			for (String str: leaguesStrs){
				int pageNum = Integer.parseInt(str);
				leagues.add(pageNum);
			}
		}

		@Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line, "\t ");           
            
			Integer pageId = 0;
        	Integer count = 0;
            
        	Boolean firstItem = true;
        	
            while (tokenizer.hasMoreTokens()) {
                String num = tokenizer.nextToken().trim().toLowerCase();
                
                if (firstItem){
        			pageId = Integer.parseInt(num.toString());
        			firstItem = false;
                }
                else{
                	count = Integer.parseInt(num.toString());
                }                
            }
			
        	if (leagues.contains(pageId)){
        		Integer[] items = {pageId, count};
        		IntArrayWritable val = new IntArrayWritable(items);
    			context.write(NullWritable.get(), val);               
        	}
		}
	}

	public static class PopularityLeagueReduce extends Reducer<NullWritable, IntArrayWritable, IntWritable, IntWritable> {
		@Override
        public void reduce(NullWritable key, Iterable<IntArrayWritable> values, Context context) throws IOException, InterruptedException {
			Map<Integer, Integer> leaguesRates = new HashMap<Integer, Integer>();
			Map<Integer, Integer> leaguesCounts = new HashMap<Integer, Integer>();
			Map<Integer, Integer> leaguesCounts2 = new HashMap<Integer, Integer>();
			
			for (IntArrayWritable val : values) {       		
				IntWritable[] pair= (IntWritable[]) val.toArray();
        		Integer pageId = pair[0].get();
        		Integer pageCount = pair[1].get();        		
    			leaguesRates.put(pageId, 0);
    			leaguesCounts.put(pageId, pageCount);
    			leaguesCounts2.put(pageId, pageCount);
			}

			for (Map.Entry<Integer, Integer> val : leaguesCounts.entrySet()) {    
        		Integer pageId = val.getKey();
        		Integer pageCount = val.getValue();        		
	    		Integer rate = 0;
				
				for (Map.Entry<Integer, Integer> val2 : leaguesCounts2.entrySet()) {       		
	        		Integer compareId = val2.getKey();
	        		Integer compareCount = val2.getValue();
	        		
	        		if (compareId != pageId && compareCount < pageCount){
	        			rate++;
	        		}
				}

				leaguesRates.put(pageId, rate);
			}					
			
			for (Map.Entry<Integer, Integer> entry : leaguesRates.entrySet())
			{
				context.write(new IntWritable(entry.getKey()), new IntWritable(entry.getValue()));
			}		
		}
	}
}