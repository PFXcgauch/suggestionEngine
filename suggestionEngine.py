# -*- coding: utf-8 -*-
"""
===============================================================================
Created on Mon Apr 15 09:19:33 2019

@author: Chris Gauch
@title: Item to Item suggestion engine
@last update: 04-17-2019
@python version: 3.7.2
@version: Alpha 1.0.0.0
===============================================================================
Queries will have to be updated to accomidate table changes
===============================================================================
"""
import psycopg2

class suggestion_engine(object):
    
    ###########################################################################
    ###########################################################################
    """
    Connects to the postrgres transactional database and execute sql statements.
    Then it will return the data set it gets from the sql statment.
    """
    def postgres(stmt):
        #Update these to connect to your instance
        var_dbname='pfxecomm'
        var_user='postgres'
        var_password='############'
        var_host='#############'
        
        conn = psycopg2.connect(dbname=var_dbname, user=var_user
                                ,password=var_password, host=var_host
                                ,port='5432') 
        cur = conn.cursor()
        
        cur.execute(stmt)
        try:
            data=cur.fetchall()
    
        except ValueError:
            raise Exception("Failed to fetch data")
    
        return data
    ###########################################################################
    ###########################################################################
    """
    This is the actual "engine" that will compare the selected data set to the 
    brand/product line.
    """
    def engine(cmpDataSet,itemnumber):
        scoreArray=[]
        #get count of attribute table.
        stmt_attributeCnt="""SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
                          WHERE TABLE_NAME='item_property'"""
        
        #gets attributes for currently viewed item. This id must be passed to
        #this class to run              
        stmt_basedata=(f"""SELECT * 
                       FROM pfxecomm.public.item_property 
                       WHERE item_number='{itemnumber}'""")
                          
        SQLreturn=suggestion_engine.postgres(stmt_attributeCnt)
        atrbCnt=int(SQLreturn[0][0])            
        
        SQLreturn=suggestion_engine.postgres(stmt_basedata)
        baseProduct=SQLreturn
        
        #this is causing delay in processing
        for row in cmpDataSet:
            scoreCnt=0
            baseColumn=0
            for column in row:
                if column==baseProduct[0][baseColumn]:
                    scoreCnt+=1 #adds one to score if the items match    
                baseColumn+=1 #adds 1 to the base col to run through base data
                
            #this will be the decimal score to match based on most like: 
            score=round(scoreCnt/atrbCnt,4) 
            scoreArray.append([row[0],score])
        
        return scoreArray #contains all brand items that 
    
    
    ###########################################################################
    ###########################################################################
    """
    Main program that collects and processes data sets.
    """
    def main(itemid):

        tileLimit=15 #Real limit will be 15
        combineArray=[] #groups all datasets together
        getArray=[] #gets data back from engine in array form
        var_score=1.0 #static score used for productline items
        items=[] #API formatted data

        #get brand and prod id
        stmt_GetprodBrand=(f"""SELECT brand_id,prodline_id 
                           FROM pfxecomm.public.item_property
                           WHERE item_number='{itemid}'""")
        
        #executing sql statement
        SQLreturn=suggestion_engine.postgres(stmt_GetprodBrand)
        
        
    
        #unpacking data and forcing to string data type
        var_prodid=str(SQLreturn[0][1])
        var_brandid=str(SQLreturn[0][0])
        
        #get base data
        stmt_basedata=(f"""SELECT specie_dog,specie_cat,specie_other
                       ,type_food, type_toy, type_litter, type_medication 
                       FROM pfxecomm.public.item_property 
                       WHERE item_number='{itemid}'""")
        #base data data point to make sure we only compare food to food etc
        data_points=suggestion_engine.postgres(stmt_basedata)
        
        
###############################################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
###############################################################################        
        #gets count of how many items share the brand:
        stmt_brandCnt=(f"""SELECT COUNT(*) 
                        FROM pfxecomm.public.item_property 
                        WHERE brand_id='{var_brandid}'
                        AND item_number<>'{itemid}'
                        AND specie_dog={data_points[0][0]}
                        AND specie_cat={data_points[0][1]}
                        AND specie_other={data_points[0][2]}
                        AND type_food={data_points[0][3]}
                        AND type_toy={data_points[0][4]}
                        AND type_litter={data_points[0][5]}
                        AND type_medication={data_points[0][6]};""")
        
        stmt_getProdLineId=(f"""SELECT item_number 
                            FROM pfxecomm.public.item_property
                            WHERE prodline_id='{var_prodid}'
                            AND item_number<>'{itemid}'
                            LIMIT {tileLimit};""")
        
        stmt_brandData=(f"""SELECT item_number 
                        FROM pfxecomm.public.item_property
                        WHERE brand_id='{var_brandid}'
                        AND item_number<>'{itemid}'
                        AND specie_dog={data_points[0][0]}
                        AND specie_cat={data_points[0][1]}
                        AND specie_other={data_points[0][2]}
                        AND type_food={data_points[0][3]}
                        AND type_toy={data_points[0][4]}
                        AND type_litter={data_points[0][5]}
                        AND type_medication={data_points[0][6]};""")
         
        #get brand id atribute data excluding product line items:
        stmt_brandAtrb=(f"""SELECT * 
                        FROM pfxecomm.public.item_property
                        WHERE brand_id='{var_brandid}' 
                        AND prodline_id<>'{var_prodid}' 
                        AND item_number<>'{itemid}'
                        AND specie_dog={data_points[0][0]}
                        AND specie_cat={data_points[0][1]}
                        AND specie_other={data_points[0][2]}
                        AND type_food={data_points[0][3]}
                        AND type_toy={data_points[0][4]}
                        AND type_litter={data_points[0][5]}
                        AND type_medication={data_points[0][6]};""")
        
        #gets count of how many items share the product line:
        stmt_prodLineCnt=(f"""SELECT COUNT(*) 
                        FROM pfxecomm.public.item_property
                        WHERE prodline_id='{var_prodid}'
                        AND item_number<>'{itemid}';""")
###############################################################################
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
###############################################################################         
        
        
        SQLreturn=suggestion_engine.postgres(stmt_prodLineCnt)
        
        prodLine_dataCnt=SQLreturn[0][0]
        prodLine_dataCnt=int(prodLine_dataCnt)

        
        SQLreturn=suggestion_engine.postgres(stmt_brandCnt)
        
        brand_dataCnt=SQLreturn[0][0]
        brand_dataCnt=int(brand_dataCnt)
        
        """
        Product line items do not need to be evaluated by the engine.  This is 
        due to the fact that they are already the most like the currently
        viewed product.  So they skip going to the engine and are given a fake
        score value of 1.0
        
        Brand items that are not in the same product line must be evaluated by
        the engine as same brand can have a lot of differences.
        
        If both the combine total for Productline & brand are less than the 
        total number of tiles we will take all of them to display.
        """
        #######################################################################
        if tileLimit<=prodLine_dataCnt:
            SQLreturn=suggestion_engine.postgres(stmt_getProdLineId)
            prodSqlData=SQLreturn 
            
            for row in prodSqlData:
                row=str(row[0])#force to string
                combineArray.append([row,var_score])
        #######################################################################      
        elif tileLimit<=prodLine_dataCnt+brand_dataCnt:
            SQLreturn=suggestion_engine.postgres(stmt_getProdLineId)
            prodSqlData=SQLreturn
            
            for row in prodSqlData:
                row=str(row[0])#force to string          
                combineArray.append([row,var_score])
           
            
            #gets brand data that is not productline and assess it
            SQLreturn=suggestion_engine.postgres(stmt_brandAtrb)
            brandSqlData=SQLreturn 
    
            getArray=suggestion_engine.engine(brandSqlData,itemid)
            
            for item in getArray:
                combineArray.append(item)
        #######################################################################   
        else:  
            brandData=suggestion_engine.postgres(stmt_brandData)
            for row in brandData:
                row=str(row[0]) #force to string
                combineArray.append([row,var_score])
        #######################################################################
        
        for item in combineArray:
            temp={} #temporary dictionary to format data for API acceptance
            temp={
                  "itemnumber" : item[0],
                  "score" : item[1]
                  }
            items.append(temp)
        return items
###############################################################################

