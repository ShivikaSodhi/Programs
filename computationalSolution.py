import csv
import numpy as np
import statistic_function_week3 as stats

def getDruggableStentFile(filename):
    csvfile=open(filename,"r")
    objContainingData=csv.reader(csvfile,delimiter=",")
    drugableStentData = list(objContainingData)
    csvfile.close()

    return drugableStentData
  
######################################################################################################################################
def calculations(stentData):
       
    dataRequired = []
          
    stentData.remove(stentData[0])      
    for i in xrange(len(stentData)):
        try:
            stentData[i][10] = float(stentData[i][10])
            stentData[i][11] = float(stentData[i][11])          
            stentData[i][13] = float(stentData[i][13])
            stentData[i][14] = float(stentData[i][14])    
            dataRequired.append(stentData[i])           
        except ValueError:
            continue

    return dataRequired

#####################################################################################################################################
def conversions(cleanedData):              
    #Setting the numpy Array:   =====>
    stentData = np.array(cleanedData);
    
    #defininf all the Lists
    dystolic_baseLine = []
    dystolic_9months = []
    stenosisBaseLine = []
    perRenalBase = []
    
    #For endPoint 1:
    dystolic_baseLine = stentData[:,10]
    dystolic_9months = stentData[:,13]    
    
    #For endPoint 2:
    stenosisBaseLine = stentData[:,11]
    perRenalBase = stentData[:,14]
    
    #Setting theirdataTypes to float
    dataType = np.dtype(float)
    dystolic_baseLine = np.array(dystolic_baseLine,dataType)
    dystolic_9months = np.array(dystolic_9months,dataType)
    stenosisBaseLine = np.array(stenosisBaseLine,dataType)
    perRenalBase = np.array(perRenalBase,dataType)

    for i in range(len(stenosisBaseLine)):
        perRenalBase[i] = (stenosisBaseLine[i] * perRenalBase[i])/100
        #print perRenalBase[i]
            
    #Calculating t_statistic for endPoint 1:
    t_stats_forEnd1 = []
    t_stats_forEnd2 = []
             
    t_stats_forEnd1 =  stats.t_statistic_welch_test(perRenalBase,stenosisBaseLine)
    t_stats_forEnd2 =  stats.t_statistic_welch_test(dystolic_baseLine,dystolic_9months)
       
    avgStenosis = np.average(dystolic_9months)
    avgDystolicBP = np.average(perRenalBase)

    #print "Values calculated using the t_statistic welsch test: \n"
    #print t_stats_forEnd1
    #print t_stats_forEnd2

    #returning the tof values for both the Endpoints
    return t_stats_forEnd1,t_stats_forEnd2,avgStenosis,avgDystolicBP
   
######################################################################################################################################
def extractTCritical(dofCalculated):
    dof_criticalFile = getDruggableStentFile("t_critical_table.csv")
    t_criticalFile = 0.0
    min_DofCritical = float("inf")
    minIndex = 0
     
    for i in range(len(dof_criticalFile)):
        try:
            if(np.absolute((float(dofCalculated))-float(dof_criticalFile[i][0])) < min_DofCritical):
                min_DofCritical = np.absolute(float(dofCalculated)-float(dof_criticalFile[i][0]))
                minIndex = i
        except:
            continue
    #print min_DofCritical
    t_criticalFile = dof_criticalFile[minIndex][1]    
    return float(t_criticalFile)

######################################################################################################################################
#Function to check whether the conditions have been met
def conditionsMet(stats_calculatedEndPoint1,stats_calculatedEndPoint2,avgStenosisPoint1,avgBPPoint2,t_critical):
    
    #This removes the heading of the file coming in   
    t_critical.remove(t_critical[0])   
    criticalDataFor1 = []
    criticalDataFor2 = []   
    
    #Converting the values in the t_critical file to float
    for i in xrange(len(t_critical)):
        try:
            t_critical[i][0] = float(t_critical[i][0])         
            t_critical[i][1] = float(t_critical[i][1])             
            criticalDataFor1.append(t_critical[i])   
            criticalDataFor2.append(t_critical[i])                   
        except ValueError:
            continue
                 
    #dof and t Calculated using t_statistic function from the t_statistic module          
    dof_calculatedEndPoint1 = stats_calculatedEndPoint1[1]
    dof_calculatedEndPoint2 = stats_calculatedEndPoint2[1]
    t_calculatedEndPoint1 = stats_calculatedEndPoint1[0]
    t_calculatedEndPoint2 = stats_calculatedEndPoint2[0]      
    
    #Calculating the adjacent critical value corresponding to the minimun of [dof in file - dof from statisics]
    calculatedCriticalFor1 =  extractTCritical(dof_calculatedEndPoint1) 
    calculatedCriticalFor2 =  extractTCritical(dof_calculatedEndPoint2)        
     
    print "\n"                    
                    
    minPercentStenosis = float(raw_input("Enter the average percentage stenosis below which the drugable stent must achieve by the end of the clinical trial:(Default is 10) ") or 10)
    minAvgBP = float(raw_input("Enter the minimum average decrease in blood pressure:(Default is 10) ") or 10)
   
        
                  
    if (t_calculatedEndPoint1<calculatedCriticalFor1):
        if (avgStenosisPoint1<=minPercentStenosis):    #avg of the 9months compare with user
           print "End point 1 has been met"
        else:
           print "End point 1 has not been met."      
    else:
        print "End point 1 has not been met"   
               

    if (t_calculatedEndPoint2<calculatedCriticalFor2):
        if (avgBPPoint2<=minAvgBP):    
           print "End point 2 has been met"
        else:
           print "End point 2 has not been met."      
    else:
        print "End point 2 has not been met"    
  
    print ""                                    
                     
#######################################################################################################################################
# Defining main now:
#######################################################################################################################################
def main():

    print "Reading the DrugableStent Data..."        
    dataSet = getDruggableStentFile("DrugableStent_ClinicalTrial_Data.csv")
    print "The file is loaded\n"
    
    #This function cleans up the Data
    cleanedData = calculations(dataSet)       
    print "Cleaning up of the data has been done\n"

    #calculating the tof for both the endPoints
    t_calculatedEndPoint1,t_calculatedEndPoint2,avgStenosisPoint1,avgBPPoint2 = conversions(cleanedData)

    #This function extracts the data from t_critical file:
    criticalData = getDruggableStentFile("t_critical_table.csv")
    print "\n Reading the t_critical Data...\n"
    
    #This function checks if the condicitons have been met
    conditionsMet(t_calculatedEndPoint1,t_calculatedEndPoint2,avgStenosisPoint1,avgBPPoint2,criticalData)

main()
#######################################################################################################################################
