import json

import pandas as pd


if __name__ == "__main__":
    base_path = '//MultitextAnalysis/report_named_entities/'
    jsonFile = open(base_path + 'entities_by_country.json')
    jsonString = jsonFile.read()
    jsonData = json.loads(jsonString)
    df = pd.DataFrame.from_dict(jsonData, orient='index')
    df_entity = pd.DataFrame()
    for index, row in df.iterrows():
        entities = row
        for each in row:
            df_entity.append(row, ignore_index=True)
    print(df_entity)
    # top_20 = df['Entity'].value_counts().head(20).to_dict()
    # top_20_new = {}
    # for key, value in top_20.items():
    #     top_20_new.update({key: {'count': value}})
    # pd.DataFrame(top_20_new).to_json('top_20_entities.json')
