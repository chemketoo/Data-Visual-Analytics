
######Please mannually install Shiny and magrittr packages in your RStudio console###### 

list.of.packages = c("shiny", "SnowballC","dplyr","GGally","tidytext","ggplot2", "wordcloud", "tm", "topicmodels", "magrittr", "rpivotTable") 
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0) {install.packages(new.packages)}
lapply(list.of.packages, require, character.only=T)


shinyServer(
  function(input,output){
    
    #Load Data
    df1 <- read.csv("Other/data_set.csv", header = TRUE)
    
    #convert the below from factor to character class
    df1$asin <- as.character(df1$asin)
    df1$reviewerID <- as.character(df1$reviewerID)
    df1$summary <- as.character(df1$summary)
    df1$reviewText <- as.character(df1$reviewText)
    
    output$dataStruct <- renderPrint({str(df1)}) #About>Data Structure tab
    
    
    #Create tokens from text and stem words
    tidy_amzn <- df1 %>%
      unnest_tokens(word, reviewText) %>%
      anti_join(stop_words) %>% # Removes stop words
      filter(word != "br") %>%
    mutate(word = wordStem(word)) #HTML tag <br /><br /> results in the word "br"
    
    
    ######################word Count vizualization#################

    #Count frequency of tokens and sort by frequency of occurrence. 
    top_Words <- tidy_amzn %>%
      count(word, sort = TRUE)
    
    datasetInput <- reactive({
      switch(input$dataset,
             "top_Words" = top_Words)
    })
    
    output$table <- renderTable({
      datasetInput()
    })
    
    #Word Count Visualization>Most Frequently Used Words in the Data Set tab
    output$topWords <- renderTable({
      topWordstbl <- top_Words[input$topWords_x[1]:input$topWords_x[2],]
      topWordstbl},include.rownames=FALSE) 
    
    output$topWordsData <- downloadHandler(
      filename = function() {
        paste(input$dataset, ".csv", sep = "")
      },
      content = function(file) {
        write.csv(datasetInput(), file, row.names = FALSE)
      }
    )
    
    #Word Count Visualization>Top words used by Product Specification tab
    var <- tidy_amzn %>%
      count(asin, product_name, word, sort = TRUE)
    
    output$tbl <- DT::renderDataTable(
      datatable(
        var, filter = 'top', rownames = FALSE,
        extensions = 'Buttons', options = list(
          dom = 'Bfrtip',
          buttons = c('copy', 'print', 'csv'))))
      
   
    
    #Word Count Visualization>Word Count Bar Chart tab  
    word_BarChart <- tidy_amzn %>%
      count(word, asin, sort = TRUE) 

    wordBarChart <- reactive({
      
      word_BarChartdf <- word_BarChart %>%
        filter(asin == input$wordBarChart1_x) %>%
        filter(n >20) %>%
        mutate(word = reorder(word, n)) 

      ggplot(word_BarChartdf, aes(word, n)) + geom_bar(stat="identity", fill="#FF9999", colour="black") + coord_flip()})
 
    output$wordBarChart1 <- renderPlot ({wordBarChart()})	
    
    #Word Count Visualization>Word cloud tab
    output$wordsCloud <- renderPlot({
      tidy_amzn %>%
        with(wordcloud(word, min.freq= input$wordsCloud_x1, max.words = input$wordsCloud_x2, scale=c(4,0.5), colors=brewer.pal(8, "Dark2")))})
    
    ##############Sentiment Analysis###########################
    
    ##AFINN
    afinn_table <- tidy_amzn %>%
      inner_join(get_sentiments("afinn"), by = "word")
    
    
    pivot_afinn <- afinn_table %>%
      select(asin, product_name,  overall_ratings, score)%>%
      group_by(asin, product_name)%>%
      summarise(avg_overallratings = mean(overall_ratings), avg_score = mean(score))%>%
      mutate_if(is.numeric, round, digits=2)
    
    #Sentiment Analysis>AFINN Results tab 1
    output$pivotafinn <- renderDT({pivot_afinn}, filter = 'top',rownames = FALSE, 
                                  extensions = 'Buttons', options = list(
                                    dom = 'Bfrtip',
                                    buttons = c('copy', 'print', 'csv')))
   
    pivot_Afinn2 <- afinn_table %>%
      select(reviewerID, overall_ratings, score)%>%
      group_by(reviewerID)%>%
      summarise(avg_overallratings = mean(overall_ratings), avg_score = mean(score))%>%
      mutate_if(is.numeric, round, digits=2)
    
    #Sentiment Analysis>AFINN Results tab 2
    output$pivotAfinn2 <- renderDT({pivot_Afinn2}, filter = 'top',rownames = FALSE,
                                   extensions = 'Buttons', options = list(
                                     dom = 'Bfrtip',
                                     buttons = c('copy', 'print', 'csv')))
    
    
    afinn_table2 <- afinn_table %>% select("overall_ratings", "score")
     
    #Sentiment Analysis>AFINN Visualization tab
    pivot_afinn1 <- rpivotTable(afinn_table2, cols = "overall_ratings", rendererName = "Line Chart", aggregatorName = "Average", vals = "score")
    
    output$pivotafinn1 <- renderRpivotTable(pivot_afinn1)
    
    #Sentiment Analysis>AFINN Visualization tab2
    pivot_afinn2 <- rpivotTable(afinn_table %>% select("score", "reviewerID"), cols = "score", rendererName = "Stacked Bar Chart", aggregatorName="Count Unique Values", vals = "reviewerID")
    
    output$pivotafinn2 <- renderRpivotTable(pivot_afinn2)
    
    #Now get average sentiment score for each asin to plot overall_ratings vs. avg_score
    afinn_avg <- afinn_table %>%
      group_by(asin) %>%
      summarise(avg_score=mean(score),
                sum_score=sum(score),
                avg_rating = mean(overall_ratings))
    

    #Visualize Results
    afinn_Plot<- ggplot(afinn_avg,
           aes(x=avg_score, y=avg_rating)) +
      geom_point(shape=1) + 
      geom_smooth(method=lm, 
                  se=TRUE) 
    
    
    #Sentiment Analysis>Visualization tab
    output$afinnPlot <- renderPlot({afinn_Plot})
    
    ##NRC
    nrc_table <- tidy_amzn %>%
      inner_join(get_sentiments("nrc"), by = "word")
    
    nrc_avg <- nrc_table %>%
      group_by(reviewerID, sentiment) %>%
      tally()
    
    output$nrc_avg1 <- renderDT({nrc_avg}, filter = 'top',rownames = FALSE,
                                extensions = 'Buttons', options = list(
                                  dom = 'Bfrtip',
                                  buttons = c('copy', 'print', 'csv')))


    #Sentiment Analysis>NRC Results tab
    output$nrcTable <- renderDT({nrc_table}, filter = 'top',rownames = FALSE,
                                extensions = 'Buttons', options = list(
                                  dom = 'Bfrtip',
                                  buttons = c('copy', 'print', 'csv')))
    
    #Sentiment Analysis>NRC Visualization tab
    pivot_nrc <- rpivotTable(nrc_table %>% select("sentiment", "reviewerID"), col = "sentiment", rendererName = "Stacked Bar Chart", aggregatorName="Count Unique Values", vals = "reviewerID")
    
    output$pivotnrc <- renderRpivotTable(pivot_nrc)
    

    ##Bing
    bing_table <- tidy_amzn %>%
      inner_join(get_sentiments("bing"), by = "word")
    
    bing_avg <- bing_table %>%
      group_by(reviewerID, sentiment) %>%
      tally()
    
    output$bing_avg1 <- renderDT({bing_avg}, filter = 'top',rownames = FALSE, 
                                 extensions = 'Buttons', options = list(
                                   dom = 'Bfrtip',
                                   buttons = c('copy', 'print', 'csv')))
    
    pivot_bing <- rpivotTable(bing_table %>% select("asin", "sentiment", "product_name"), rows = c("asin"), cols = c("sentiment" ), rendererName = "Heatmap")
    
    #Sentiment Analysis>Bing Results tab
    output$bingTable <- renderRpivotTable(pivot_bing)
    
    #Sentiment Analysis>Bing Visualization tab 
    pivot_bing2 <- rpivotTable(bing_table %>% select("sentiment", "reviewerID"), cols = c("sentiment" ), rendererName = "Stacked Bar Chart", aggregatorName="Count Unique Values", vals = "reviewerID")
    
    output$pivotbing2 <- renderRpivotTable(pivot_bing2)

    ##############Topic Models###########################
    amzn_dtm <- tidy_amzn %>%
      count(asin, word, sort = TRUE) %>%
      ungroup() %>%
      cast_dtm(asin, word, n)
    
    #Topic Models>LDA Visualization tab
    output$topicsPlot <- renderPlot({
      
      product_lda <- LDA(amzn_dtm, k = input$topicsPlot_x1, control = list(seed = 1234))
      product_topics <- tidy(product_lda, matrix = "beta")
      
      top_terms <- product_topics %>%
        group_by(topic) %>%
        top_n(input$topicsPlot_x2, beta) %>%
        ungroup() %>%
        arrange(topic, -beta)
      
      top_terms %>%
        mutate(term = reorder(term, beta)) %>%
        ggplot(aes(term, beta, fill = factor(topic))) +
        geom_col(show.legend = FALSE) +
        facet_wrap(~ topic, scales = "free") +
        coord_flip()})

})  
    
    

    
  



    


    
                            
    





    

    

    


    
      
      
      
      
      
      
      
      
      
      
      
      
    
      
      
      
      
  
