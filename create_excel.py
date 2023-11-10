import pandas as pd
from bs4 import BeautifulSoup as bs

#Criando objeto BS
def get_file(file_name):
    content = []
    with open(file_name, 'r') as file:
        content = file.readlines()
        content = ''.join(content)
        soup = bs(content,'xml')
    return soup

#Buscando parents
def get_parents(soup):
    parents = []
    for p in soup.parents:
        if p.has_attr("NAME") and p.find('TRANSFORMATION'):
            parents.append(p["NAME"])
    return parents

#Buscando valores
def get_values(soup, tag1):
    mapping = soup.find_all(tag1)
    names = []
    descriptions = []
    parents = []
    for map in mapping:
        names.append(map.get('NAME'))
        descriptions.append(map.get('DESCRIPTION'))
        parents.append(get_parents(map)) #soup>map
    list_values = [parents, names, descriptions]
    return list_values

#Criando DF
def create_df(list_values):
    dict = {
        'PARENTS': list_values[0],
        'NAME': list_values[1],
        'DESCRIPTION': list_values[2]
    }
    df = pd.DataFrame(dict)
    return df

#Criando excel
def create_file(filename, df):
    return df.to_excel(excel_writer=filename, sheet_name=filename, header=True)

#Separando colunas
def transform_column_parents(file):
    df_origin = pd.read_excel(file)
    list_column = df_origin['PARENTS'].values.tolist()
    list_column = [eval(item) for item in list_column]
    try:
        df_column = pd.DataFrame(list_column, columns=['MAPPING', 'FOLDER', 'REPOSITORY'])
        df_clean = df_origin.drop(['PARENTS'], axis=1)
        df_clean = df_origin.drop(['Unnamed: 0'], axis=1)
        df_complete = pd.concat([df_column, df_clean], axis=1)
    except:
        df_column = pd.DataFrame(list_column, columns=['FOLDER', 'REPOSITORY'])
        df_clean = df_origin.drop(['PARENTS'], axis=1)
        df_clean = df_origin.drop(['Unnamed: 0'], axis=1)
        df_complete = pd.concat([df_column, df_clean], axis=1)
    else: 
        print('working')
        df_clean = df_origin.drop(['PARENTS'], axis=1)
        df_clean = df_origin.drop(['Unnamed: 0'], axis=1)
        df_complete = pd.concat([df_column, df_clean], axis=1)
    return df_complete

if __name__ == '__main__':
    #Strings
    name = '../mapping.XML'
    tag_mapping = 'MAPPING'
    tag_transformation = 'TRANSFORMATION'
    tag_target = 'TARGET'
    tag_source = 'SOURCE'
    filename_mapping = 'mapping.xlsx'
    filename_transformation = 'transformation.xlsx'  
    filename_target = 'target.xlsx'           
    filename_source = 'source.xlsx'   
    
    #Criando objeto soup
    soup = get_file(name)
    
    #buscando valores de mapping, criando df e criando xlsx
    list_mapping = get_values(soup, tag_mapping)
    df_mapping = create_df(list_mapping)
    create_file(filename_mapping, df_mapping)
    
    #buscando valores de transformation, criando df e criando xlsx
    list_transformation = get_values(soup, tag_transformation)
    df_transformation = create_df(list_transformation) 
    create_file(filename_transformation, df_transformation)
   
    #buscando valores de target, criando df e criando xlsx
    list_target = get_values(soup, tag_target)
    df_target = create_df(list_target)
    create_file(filename_target, df_target)
    
    #buscando valores de source, criando df e criando xlsx
    list_source = get_values(soup, tag_source)
    df_source = create_df(list_source)
    create_file(filename_source, df_source)
    
    #Bloco para dividir em tabelas os parents
    file1 = '../source.xlsx'
    file2 = '../mapping.xlsx'
    file3 = '../transformation.xlsx'
    file4 = '../target.xlsx'

    #Sources
    df1 = transform_column_parents(file1)
    create_file(df1, 'source.xlsx')

    #Mappings
    df2 = transform_column_parents(file2)
    create_file(df2, 'mapping.xlsx')

    #Transformations
    df3 = transform_column_parents(file3)
    create_file(df3, 'transformation.xlsx')

    #Targets
    df4 = transform_column_parents(file4)
    create_file(df4, 'target.xlsx')