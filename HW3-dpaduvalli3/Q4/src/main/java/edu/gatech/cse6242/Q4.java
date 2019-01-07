package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {
  static class firstMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable>{@Override
  		public void map(LongWritable key, Text value, Context context)
  				throws IOException, InterruptedException{
  					String rawData = value.toString();
            if(rawData.length()>1){
  					String[] newData = rawData.split("\t");
  					IntWritable src = new IntWritable(Integer.parseInt(newData[0]));
  					IntWritable tgt = new IntWritable(Integer.parseInt(newData[1]));
  					IntWritable plus1 = new IntWritable(1);
  					IntWritable negative1 = new IntWritable(-1);
  					context.write(src, plus1);
  					context.write(tgt, negative1);}}}
          	
  static class secondMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable>{@Override
  		public void map(LongWritable key, Text value, Context context)
  				throws IOException, InterruptedException{
  					String rawData = value.toString();
            if(rawData.length()>1){
  					String[] newData = rawData.split("\t");
  					IntWritable degreeDiff = new IntWritable(Integer.parseInt(newData[1]));
  					IntWritable plus1 = new IntWritable(1);
  					context.write(degreeDiff, plus1);}}}
  						
  static class totalReducer extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable>{@Override
  		public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) 
  				throws IOException, InterruptedException{
  					int initTotal = 0;
  					for(IntWritable value: values)
  						initTotal += value.get();
  					context.write(key, new IntWritable(initTotal));}}

  public static void main(String[] args) throws Exception {
    Configuration config1 = new Configuration();
    String output_Dirpath = args[1]+"-output_Dirpath";
    
    /* TODO: Needs to be implemented */
    Job createJobInst1 = Job.getInstance(config1, "Q4part1");
    createJobInst1.setJarByClass(Q4.class);
    createJobInst1.setMapperClass(firstMapper.class);
    createJobInst1.setReducerClass(totalReducer.class);
    createJobInst1.setOutputKeyClass(IntWritable.class);
    createJobInst1.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(createJobInst1, new Path(args[0]));
    FileOutputFormat.setOutputPath(createJobInst1, new Path(output_Dirpath));
    createJobInst1.waitForCompletion(true);

    Configuration config2 = new Configuration();
    Job createJobInst2 = Job.getInstance(config2, "Q4part2");
    createJobInst2.setJarByClass(Q4.class);
    createJobInst2.setMapperClass(secondMapper.class);
    createJobInst2.setReducerClass(totalReducer.class);
    createJobInst2.setOutputKeyClass(IntWritable.class);
    createJobInst2.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(createJobInst2, new Path(output_Dirpath));
    FileOutputFormat.setOutputPath(createJobInst2, new Path(args[1]));
    System.exit(createJobInst2.waitForCompletion(true)?0:1);}}


          
  				
  		
