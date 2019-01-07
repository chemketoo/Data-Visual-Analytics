// Databricks notebook source
// MAGIC %md
// MAGIC #### Q2 - Skeleton Scala Notebook
// MAGIC This template Scala Notebook is provided to provide a basic setup for reading in / writing out the graph file and help you get started with Scala.  Clicking 'Run All' above will execute all commands in the notebook and output a file 'toygraph.csv'.  See assignment instructions on how to to retrieve this file. You may modify the notebook below the 'Cmd2' block as necessary.
// MAGIC 
// MAGIC #### Precedence of Instruction
// MAGIC The examples provided herein are intended to be more didactic in nature to get you up to speed w/ Scala.  However, should the HW assignment instructions diverge from the content in this notebook, by incident of revision or otherwise, the HW assignment instructions shall always take precedence.  Do not rely solely on the instructions within this notebook as the final authority of the requisite deliverables prior to submitting this assignment.  Usage of this notebook implicitly guarantees that you understand the risks of using this template code. 

// COMMAND ----------

/*
DO NOT MODIFY THIS BLOCK
This assignment can be completely accomplished with the following includes and case class.
Do not modify the %language prefixes, only use Scala code within this notebook.  The auto-grader will check for instances of <%some-other-lang>, e.g., %python
*/
import org.apache.spark.sql.functions.desc
import org.apache.spark.sql.functions._
case class edges(Source: String, Target: String, Weight: Int)
import spark.implicits._

// COMMAND ----------

/* 
Create an RDD of graph objects from our toygraph.csv file, convert it to a Dataframe
Replace the 'toygraph.csv' below with the name of Q2 graph file.
*/

val df = spark.read.textFile("/FileStore/tables/bitcoinalpha.csv") 
  .map(_.split(","))
  .map(columns => edges(columns(0), columns(1), columns(2).toInt)).toDF()


// COMMAND ----------

// e.g. eliminate duplicate rows
val new_df = df.dropDuplicates()


// COMMAND ----------

// e.g. filter nodes by edge weight >= supplied threshold in assignment instructions

val filtered_df = new_df.filter("Weight >= 5")


// COMMAND ----------

val out_degree = filtered_df.groupBy($"Source")
  .agg(count("Source"))
  .withColumnRenamed("count(Source)", "outDegree")
  .withColumnRenamed("Source", "Vertex")

val in_degree = filtered_df.groupBy($"Target")
 .agg(count("Target"))
 .withColumnRenamed("count(Target)", "inDegree")
 .withColumnRenamed("Target", "Vertex")

val joined_table = out_degree.join(in_degree, Seq("Vertex"), "outer")
  .na.fill(Map("outDegree" -> 0, "inDegree" -> 0))
  .withColumn("totalDegree", $"outDegree" + $"inDegree") 

// find node with highest in-degree, if two or more nodes have the same in-degree, report the one with the lowest node id
/////////Out Degree//////////////
val minVertexMaxOd = joined_table
  .groupBy($"outDegree")
  .agg(min("Vertex"))

val high_outDegreeDf = minVertexMaxOd.select($"min(Vertex)", $"outDegree")
  .orderBy($"outDegree".desc)
  .withColumnRenamed("min(Vertex)", "v")
  .withColumnRenamed("outDegree", "d")
  .withColumn("c", lit("o"))
  .limit(1)

// find node with highest out-degree, if two or more nodes have the same out-degree, report the one with the lowest node id
/////////In Degree//////////////
val minVertexMaxIn = joined_table
  .groupBy($"inDegree")
  .agg(min("Vertex"))


val high_inDegreeDf = minVertexMaxIn.select($"min(Vertex)", $"inDegree")
  .orderBy($"inDegree".desc)
  .withColumnRenamed("min(Vertex)", "v")
  .withColumnRenamed("inDegree", "d")
  .withColumn("c", lit("i"))
  .limit(1)

// find node with highest total degree, if two or more nodes have the same total degree, report the one with the lowest node id
/////////Combined Degree//////////////
val combinedDf = joined_table
  .groupBy($"totalDegree")
  .agg(min("Vertex"))

val high_tDegreeDf = combinedDf.select($"min(Vertex)", $"totalDegree")
  .orderBy($"totalDegree".desc)
  .withColumnRenamed("min(Vertex)", "v")
  .withColumnRenamed("totalDegree", "d")
  .withColumn("c", lit("t"))
  .limit(1)


val final_df = high_outDegreeDf.union(high_inDegreeDf).union(high_tDegreeDf)


// COMMAND ----------

/*
Create a dataframe to store your results
Schema: 3 columns, named: 'v', 'd', 'c' where:
'v' : vertex id
'd' : degree calculation (an integer value.  one row with highest in-degree, a row w/ highest out-degree, a row w/ highest total degree )
'c' : category of degree, containing one of three string values:
                                                'i' : in-degree
                                                'o' : out-degree                                                
                                                't' : total-degree
- Your output should contain exactly three rows.  
- Your output should contain exactly the column order specified.
- The order of rows does not matter.
                                                
A correct output would be:

v,d,c
2,3,i
1,3,o
2,6,t


whereas:
- Node 1 has highest in-degree with a value of 3
- Node 2 has highest out-degree with a value of 3
- Node 2 has highest total degree with a value of 6
*/

// COMMAND ----------

display(final_df)
