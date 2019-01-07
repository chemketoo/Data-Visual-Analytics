DESCRIPTION:
Our package allows users to evaluate and analyze the sentiment of product reviews. We used a static dataset of reviews from Amazon to build the models. 
Users will be able to manipulate graphs, sort the data by product name, average overall rating, average score and asin (amazon id number). 

Word Count Visualization: 
The most frequently used words in the dataset tab allows users to view the most frequently used words in the data set. 
Users can select how many words to view in the list and which words to view.

Top words used by product specification tab allows users to use an interactive table to filter, sort, or search for a specific product in the search boxes. 
For example, if you paste B00000J1V5 in the asin search box, you will find the list of all the tokenized words and its counts associated with the user review. 
In the bottom 'Showing 1 to 10 of 753 entries filtered from 12,328 total entries', you will find the total number of tokenized words associated for that particular product.

The word count bar chart tab shows a bar chart by asin of the top words used for that asin.

The word cloud tab is an interactive interface for users to create a word cloud by specifying the minimum frequency of the words used in the cloud and 
the maximum number of words for building the cloud.

Sentiment Analysis:
This section contains multiple tabs for users to interact and view the analysis of the sentiment of reviews. 
There are tables, charts, and many types of graphs the user can explore to obtain a better picture of the actual sentiment of a reviewer or for a product.

Topic Models:
This section contains the Latent Dirichlet Allocation (LDA) visualization.  The user selects the number of topics (each produces a horizontal bar chart) 
and the number of words (up to 10) on each graph, giving the user an idea of the most frequently used words in the reviews.


INSTALLATION:
Prerequisites
• In order to run our application, you will need to install R and R studio on your computer. Install the latest version of RStudio. 
R and RStudio Installation Instructions 

Windows Users
To Install R:
1. Open an internet browser and go to www.r-project.org.
2. Click the "download R" link in the middle of the page under "Getting Started."
3. Select a CRAN location (a mirror site) and click the corresponding link.  
4. Click on the "Download R for Windows" link at the top of the page.  
5. Click on the "install R for the first time" link at the top of the page.
6. Click "Download R for Windows" and save the executable file somewhere on your computer.  Run the .exe file and follow the installation instructions.  
7. Now that R is installed, you need to download and install RStudio.
To Install RStudio:
1. Go to www.rstudio.com and click on the "Download RStudio" button.
2. Click on "Download RStudio Desktop."
3. Click on the version recommended for your system, or the latest Windows version, and save the executable file.  Run the .exe file and follow the installation instructions.  
   
Mac Users
To Install R:
1. Open an internet browser and go to www.r-project.org.
2. Click the "download R" link in the middle of the page under "Getting Started."
3. Select a CRAN location (a mirror site) and click the corresponding link.
4. Click on the "Download R for (Mac) OS X" link at the top of the page.
5. Click on the file containing the latest version of R under "Files."
6. Save the .pkg file, double-click it to open, and follow the installation instructions.
7. Now that R is installed, you need to download and install RStudio.
To Install RStudio:
1. Go to www.rstudio.com and click on the "Download RStudio" button.
2. Click on "Download RStudio Desktop."
3. Click on the version recommended for your system, or the latest Mac version, save the .dmg file on your computer, double-click it to open, and then drag and drop it to your applications folder.


EXECUTION:
Team 16 Web App Instructions:
1. Unzip team16final folder and go to CODE.
2. Open server.R and ui.R. 
3. Ensure you set the working directory to the CODE Folder (this can be done by going to Session at the top and select Set Working Dirctory).
4. In either server.R or ui.R, manually install shiny and magrittr packages (install button is on bottom right of the RStudio console).
5. Next, click on Run App at the top right side of RStudio console (wait for a few seconds for the app to be rendered).
6. Once the app is running, you should see a screen with About, Word Count Visualization, Sentiment Analysis, and Topic Model menu options across the top.
7. You can either view our app in the default RStudio browser or open in your computer’s browser. To open in your computer’s browser, click on Open in Browser at the top left of our app screen. 
(Note: If you are having a difficulty opening our app, mannually download and load packages listed at the top of server.R and ui.R.)

