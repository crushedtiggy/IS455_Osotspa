import pandas as pd
import re

# test comments

def change_set(x):
    x = str(x)
    tmp = re.split('{|}', x)
    tmp_set = [code.strip() for code in tmp[1].split(',')]
    final_set = []
    for code in tmp_set:
        code = re.sub("[^0-9]", "", code)
        final_set.append(code)
    final_set = [int(code) for code in final_set]
    return final_set

def get_recent_SKUs(customerCode: str, sample_df: pd.DataFrame):
    cust_df = sample_df[sample_df['CustomerCode'] == customerCode]
    custSKUs = cust_df['ProductCode'].unique().tolist()
    return custSKUs

def get_product_history(customerCode: str, sample_df: pd.DataFrame):
    cust_df = sample_df[sample_df['CustomerCode'] == customerCode]
    product_qty = cust_df.groupby(['ProductCode'])['BaseQty'].sum()
    product_amt = cust_df.groupby(['ProductCode'])['NetAmount'].sum()
    return (product_qty, product_amt)

def get_recommendations(custSKUs: list, top_x: int, df: pd.DataFrame) -> dict:
    # Initialize empty list to store recommended products
    recommendations = {}
    i = 0
    
    while len(recommendations) < top_x and i < df.shape[0]:
        antecedents = df.iloc[i].antecedents
        consequents = df.iloc[i].consequents
        confidence = df.iloc[i].confidence
        
        if set(antecedents).issubset(set(custSKUs)) and not set(consequents).issubset(set(custSKUs)):
            for code in consequents:
                if code not in recommendations.keys():
                    recommendations[code] = confidence
                else:
                    recommendations[code] += confidence
        i += 1
    
    return recommendations