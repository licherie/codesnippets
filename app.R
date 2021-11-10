require("httr")
require("jsonlite")
require("readxl")
require("data.table")
require("dplyr")

#import names of counties, states, and FIPS 
my_counties <- read_excel("fips_counties_of_interest_new.xlsx")

#add column for the api urls 
source("my_key.R")
my_token = my_key

paste_calls <- function(fips_code) {
    paste0("https://api.covidactnow.org/v2/county/", fips_code, 
           ".json?apiKey=", my_token)
}

my_counties_2 <- my_counties %>% mutate(my_calls = paste_calls(fips_padded))

#add function to get data from response 
my_api_call <- function(api_call) { 
    print(api_call)
    my_info <-fromJSON(api_call)
    my_data <- c(
        api_call,
        #overall risk level
        if(is.null(my_info$riskLevels$overall)){
            "Not Available"
        } else if(my_info$riskLevels$overall == "" | is.na(my_info$riskLevels$overall)){
            "Not Available"
        } else {
            my_info$riskLevels$overall
        },
        #daily new cases
        if(is.null(my_info$actuals$newCases)){
            "Not Available"
        } else if(my_info$actuals$newCases == "" | is.na(my_info$actuals$newCases)){
            "Not Available"
        } else {
            my_info$actuals$newCases
        },
        #daily new cases per 100k
        if(is.null(my_info$metrics$caseDensity)){
            "Not Available"
        } else if(my_info$metrics$caseDensity == "" | is.na(my_info$metrics$caseDensity)){
            "Not Available"
        } else {
            my_info$metrics$caseDensity
        },
        #infection rate
        if(is.null(my_info$metrics$infectionRate)){
            "Not Available"
        } else if(my_info$metrics$infectionRate == "" | is.na(my_info$metrics$infectionRate)){
            "Not Available"
        } else {
            my_info$metrics$infectionRate
        },
        #positive test rate
        if(is.null(my_info$metrics$testPositivityRatio)){
            "Not Available"
        } else if(is.na(my_info$metrics$testPositivityRatio) | my_info$metrics$testPositivityRatio == "" ) {
            "Not Available"
        } else {
            my_info$metrics$testPositivityRatio
        },
        #% vaccinated with one dose
        if(is.null(my_info$metrics$vaccinationsInitiatedRatio)){
            "Not Available"
        } else if(my_info$metrics$vaccinationsInitiatedRatio == "" | is.na(my_info$metrics$vaccinationsInitiatedRatio)){
            "Not Available"
        } else {
            my_info$metrics$vaccinationsInitiatedRatio
        },
        #% fully vaccinated.
        if(is.null(my_info$metrics$vaccinationsCompletedRatio)){
            "Not Available"
        } else if(my_info$metrics$vaccinationsCompletedRatio == "" | is.na(my_info$metrics$vaccinationsCompletedRatio)){
            "Not Available"
        } else {
            my_info$metrics$vaccinationsCompletedRatio
        }
        # ,
        # if(is.null(my_info$cdcTransmissionLevel)){
        #     "Not Available"
        # } else if(my_info$cdcTransmissionLevel == "" | is.na(my_info$cdcTransmissionLevel)){
        #     "Not Available"
        # } else {
        #     my_info$cdcTransmissionLevel
        # }
    )
    return(my_data)
}
#apply api calls and get results
my_result<- lapply(my_counties_2$my_calls, my_api_call)
results_combined<-as.data.frame(do.call(rbind,my_result))
names(results_combined) <- c("api_call", "RiskLevel", "NewCases", "NewCasesper100k" ,
                             "InfectionRate", 
                             "PositiveRate", "VaccinationsInitiatedRatio", 
                             "VaccinationsCompletedRatio"
                             #, "cdcTransmissionLevel"
                             )

my_final_result <- my_counties_2 %>% 
    left_join(results_combined, by = c("my_calls" = "api_call"), keep = FALSE) %>%
    select(-c("my_calls"))

server <- shinyServer(function(input, output, session) {
    
    output$table<-renderTable(my_final_result)
    
    output$downloadData <- downloadHandler(
        filename = function() { 
            paste("covid-data-actNow", Sys.Date(), ".csv", sep="")
        },
        content = function(file) {
            write.csv(my_final_result, file)
        })
})

ui <- shinyUI(fluidPage(
    tableOutput("table"),
    downloadButton('downloadData', 'Download data')
))

shinyApp(ui=ui,server=server)