
######Please mannually install Shiny and magrittr packages in your RStudio console######

list.of.packages = c("shiny", "SnowballC" ,"dplyr","tidytext" , "magrittr", "DT", "rpivotTable", "shinythemes") 
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0) {install.packages(new.packages)}
lapply(list.of.packages, require, character.only=T)


#Load Data
df1 <- read.csv("Other/data_set.csv", header = TRUE)

#convert the below from factor to character class
df1$asin <- as.character(df1$asin)
df1$reviewerID <- as.character(df1$reviewerID)
df1$summary <- as.character(df1$summary)
df1$reviewText <- as.character(df1$reviewText)


#Create tokens from text and stem words
tidy_amzn <- df1 %>%
  unnest_tokens(word, reviewText) %>%
  anti_join(stop_words) %>% # Removes stop words
  filter(word != "br") %>%
  mutate(word = wordStem(word)) #HTML tag <br /><br /> results in the word "br"


word_BarChart <- tidy_amzn %>%
  count(word, asin, sort = TRUE) 
 

shinyUI(fluidPage(theme = shinytheme("united"),
  navbarPage(
    "Navigation Bar",
    ######About######
    tabPanel("About",
      titlePanel(title = "Team 16: Amazon Electronic Product Reviews Sentiment Analysis Web Application"),      
      mainPanel(
        tabsetPanel(type = "tab",
          tabPanel( "Overview", fluidRow(column(12, includeMarkdown("other/project_desc.html")))),
          tabPanel("Data Stucture", h5("Below is the structure of our data frame. We have converted ASIN, Review ID, Summary, and Review Text from Factor to Character class in order to do Sentiment Analysis."),
                    verbatimTextOutput("dataStruct")
                   )))),
    
    ########Word Count Visualization#########
    tabPanel("Word Count Visualization",
        tabsetPanel(type = "tab",
          tabPanel("About Word Count Visualization", fluidRow(column(12, includeMarkdown("other/wordVis_desc.html")))), 
          
          ###### 
          tabPanel("Most Frequently Used Words in the Data Set", 
            sidebarLayout(
              sidebarPanel("",
                sliderInput("topWords_x", label = "Top Frequently Occurring Words", min = 1,max = 50, step = 1, value = c(1, 5)),
                selectInput("dataset", "Download this Data", choices = c("top_Words")),
                downloadButton('topWordsData', 'Download Table')),
              mainPanel(tableOutput("topWords")))),
          
          ###### 
          tabPanel("Top words used by Product Specification", 
                   h5("In this interactive table, you can filter, sort, or search for a specific product in the search boxes. For example, if you paste B00000J1V5 in the asin search box, you will find the list of all the tokenized words and its counts associated with the user review. In the bottom 'Showing 1 to 10 of 753 entries filtered from 12,328 total entries', you will find the total number of tokenized words associated for that particular product."),
                   h5("Please ensure to Open in Browser to download as CSV"), DT::dataTableOutput('tbl')),
                                      
          ######         
          tabPanel("Word Count Bar Chart", 
            sidebarLayout(
              sidebarPanel("",
                selectInput("wordBarChart1_x", "Select or enter an ASIN Number", choices= word_BarChart[2], selected = "class")),
              mainPanel(h4("Top Used Words by ASIN Number"), plotOutput("wordBarChart1"), h5("To download, right click on the visualization and select save image")))),
  
          ###### 
          tabPanel("Word Cloud", 
          sidebarLayout(
            sidebarPanel("",
              sliderInput("wordsCloud_x1", label = "Minimum Frequency:", min = 1, max = 50, value=25),
              sliderInput("wordsCloud_x2", label = "Maximum Number of Words:", min = 1, max = 300, value=150)),
            mainPanel(h5("To download, right click on the visualization and select save image"), plotOutput("wordsCloud", width = "800", height = "500")))))),           
          

    ########Sentiment Analysis######
    tabPanel("Sentiment Analysis",
      mainPanel(
        tabsetPanel(type = "tab",
          tabPanel("About Sentiment Analysis", fluidRow(column(12, includeMarkdown("other/sentiment_desc.html")))),
          tabPanel("AFINN Results Table 1", h5("In this interactive table, you can view the average AFINN sentiment score and average user rating for each product."),
                   h5("Please ensure to Open in Browser to download as CSV"), DTOutput('pivotafinn')),
          tabPanel("AFINN Results Table 2", h5("In this interactive table, you can view the average AFINN sentiment score and average user rating for each reviewerID."),
                   h5("Please ensure to Open in Browser to download as CSV"),DTOutput('pivotAfinn2')),
          tabPanel("AFINN Visualization 1", h5("To download, right click and select Open Frame, go to the visualization and click on the print icon at top right of the screen and save the visualization."), rpivotTableOutput("pivotafinn1")),
          tabPanel("AFINN Visualization 2", h5("To download, right click and select Open Frame, go to the visualization and click on the print icon at top right of the screen and save the visualization."), rpivotTableOutput("pivotafinn2")),
          tabPanel("NRC Results Table 1", h5("In this interactive table, you can view the NRC sentiment predicted for each tokenized word from product reviews.  For example, if you search 9984984354, you will find a list of all the predicted sentiments for each tokenized word from the user reviews given for that product."),
                   h5("Please ensure to Open in Browser to download as CSV"),DTOutput("nrcTable")),
          tabPanel("NRC Results Table 2", h5("In this interactive table, you can view the aggregate NRC sentiment predicted for each reviewerID."),
                   h5("Please ensure to Open in Browser to download as CSV"), DTOutput("nrc_avg1")),
          tabPanel("NRC Visualization",  h5("To download, right click and select Open Frame, go to the visualization and click on the print icon at top right of the screen and save the visualization."),rpivotTableOutput("pivotnrc")),
          tabPanel("Bing Results Table 1", h5("In this interactive heatmap table, you can view the total Bing positive/negative sentiments predicted for each product. You can sort or filter asin or sentiment icons to search for a specific product."),
                   rpivotTableOutput("bingTable")),
          tabPanel("Bing Results Table 2",           h5("In this interactive table, you can view the total positive or negative sentiment count for each reviewerID."), h5("Please ensure to Open in Browser to download as CSV"), DTOutput("bing_avg1")),
          tabPanel("Bing Visualization", h5("To download, right click and select Open Frame, go to the visualization and click on the print icon at top right of the screen and save the visualization."),rpivotTableOutput("pivotbing2"))
          

          
          ))),
                   
    
    #######Topic Models#######
    tabPanel("Topic Models",
      titlePanel(title = "Latent Dirichlet Allocation (LDA)"),
      tabsetPanel(type = "tab",
        tabPanel("About LDA", fluidRow(column(12, includeMarkdown("other/lda_desc.html")))),
        tabPanel("LDA Visualization", 
          sidebarLayout(
            sidebarPanel("",
              sliderInput("topicsPlot_x1", label = "Select Number of Topics:", min = 1, max = 10, value=4),
              sliderInput("topicsPlot_x2", label = "Select Number of Words:", min = 1, max = 10, value=5)),
            mainPanel(h5("Note: When viewing this visualization please allow a few seconds for it to render"), h5("To download, right click on the visualization and select save image"), plotOutput("topicsPlot"))))))
            

  )))



  
  
  
  


