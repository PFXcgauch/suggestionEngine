# -*- coding: utf-8 -*-
"""
===============================================================================
Created on Fri Mar 22 15:19:33 2019

@author: Chris Gauch
@title: Item to Item suggestion engine
@last update: 03-27-2019
@python version: 3.7.2
@version: Alpha 1.0.0.0
===============================================================================
LOGIC:
    
Pull item I and viewing 

Pull count of product line
    IF: product line count >= limit_of_titles
        THEN: Grab top 5 product line
    ELSE:
        Get all product line
        Pull dataset of items in same brand
        IF: Brand+productline <= TitleLimit 
            THEN: Grab all
        ELSE:
            Run Engine
            Return engine data set
            Grab top tileLimit-ProductLine items
===============================================================================
"""

#imported libraries for program
import psycopg2


###############################################################################
###############################################################################
"""
Connects to the postrgres transactional database and execute sql statements.
Then it will return the data set it gets from the sql statment.
"""
def postgresSql(stmt):
    #connection to postgres on PA machine
    conn = psycopg2.connect(dbname='pfxecomm', user='postgres'
                            ,password='PFXdata123!', host='192.168.20.20'
                            ,port='5432') 
    cur = conn.cursor()
    
    cur.execute(stmt)
    data=cur.fetchall()
    
    print(data)
    return data
    

###############################################################################
###############################################################################
"""
Check the temp data table and make sure it is blank.  If it is not then it 
clears the data out.  If it can not then it sends a status back to the main
function.  if status is 0 then it errors out throwing unable to clear/data is 
not clear.
"""
def clearData():
    stmt_suggestionCnt="SELECT COUNT(*) FROM tempSuggestion;"
    SQLreturn=postgresSql(stmt_suggestionCnt)
    count=SQLretunr[0][0]
    count=int(count)
    
    status=0
    
    if count>0:
        stmt_clearData="DELETE FROM tempSuggestion;"
        try:
            postrgres(stmt_clearData)
        except:
            return status
        status=1
    else:
        status=1
    return status


###############################################################################
###############################################################################
"""
This is the actual engine that will match the selected data set to the brand/
product line.  
"""
def suggestionEngine(baseProduct,cmpDataSet):
    #get count of attribute table
    stmt_attributeCnt=""
    SQLreturn=postgresSql(stmt_attributeCnt)
    atrbCnt=SQLreturn[0][0]
    atrbCnt=int(atrbCnt)
    
    baseRow=0
    baseColumn=0
    scoreCnt=0
    
    for row in cmpDataSet:
        baseColumn=0
        for column in row:
            if column==baseProduct[baseRow][baseColumn]:
                scoreCnt+=1
                baseColumn+=1
        
            #need to store the count before jumping to the next row of data
            #get the product ID and store the score into a table
            #table will need to be wiped after every run 
            
        #this will be the decimal score to match based on most like:    
        score=scoreCnt/atrbCnt 
        #inserts score to the temp table that we will create to store the data
        stmt_insertScore=(f"""INSERT INTO tempSuggestion(score) 
                         VALUES ({score}) 
                         WHERE itemNumber={};""")
        
        postrgresSql(stmt_insertScore)
        
                        
    return score
###############################################################################
###############################################################################
"""
Main program that collects and processes data sets.
"""
def Main():
    #gets count of how many items share the product line:
    stmt_prodLineCnt=(f"""SELECT COUNT(*) 
                    FROM pfxecomm.public.{} 
                    WHERE productLineId={};""")
    #gets count of how many items share the brand:
    stmt_brandCnt=(f"""SELECT COUNT(*) 
                    FROM pfxecomm.public.{} 
                    WHERE brandid={};""")
    #gets attribute data for brand:
    stmt_brandData=(f"""SELECT * 
                    FROM pfxecomm.public.{} 
                    WHERE brandid={};""")
    #gets attribute data for product line:
    stmt_prodLineData=(f"""SELECT * 
                       FROM pfxecomm.public.{} 
                       WHERE productLineId={};""")
    
    status=clearData()
    
    if status==0: 
        print("""Error:  data has not been cleared in database. 
              Please clear manually then try again.""")
        return None
    else:
        tileLimit=10  #need to know this before go live
        SQLreturn=postgresSql(stmt_prodLineCnt)
        
        prodLine_dataCnt=SQLreturn[0][0]
        prodLine_dataCnt=int(prodLine_dataCnt)
        
        if prodLine_dataCnt>=tileLimit:
            SQLreturn=postgresSql(stmt_prodLineData)
            prodLine_data=SQLreturn
            for row in prodLine_data:
                #may need to format data
                #place holder sql statement:
                stmt_insertProdLine=(f"""INSERT INTO tempSuggestion(IMITID
                ,Score) VALUES({prodLine_data[0][0]},{prodLine_data[0][1]};""")
                #skip engine
        else:
            SQLreturn=postgresSql(stmt_brandCnt)
            brand_dataCnt=SQLreturn[0][0]
            brand_dataCnt=int(brand_dataCnt)
            if brand_dataCnt+prodLine_dataCnt<=tileLimit:
                SQLreturn=postgresSQL(stmt_brandData)
                brand_data=SQLreturn
                #skip Engine
            else:
                SQLreturn=postgresSQL(stmt_brandData)
                brand_data=SQLreturn
                #run Engine
                
    return None
