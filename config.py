class Config:
    # filepath = os.path.abspath(pkg_resources.resource_filename('__main__', '/MultitextAnalysis/'))
    filepath = '/Users/geminiwenxu/PycharmProjects/MultitextAnalysis/'
    data_path = filepath + 'Data/'
    reports_path = data_path + 'reports/'
    keywords = ['covid-19', 'corona', 'coronavirus', 'socialdistance', 'socialdistancing', 'globalpandemic',
                'stayathome', 'FightCOVID19', 'covid', 'outbreak', 'crisis', 'virus', '#conronavirus', '#covid',
                'Coronavirus', 'Covid-19', 'Corona']
    country_prefix = ['aus_', 'cn_', 'de_', 'fr_', 'jp_', 'kr_', 'nl_', 'se_', 'sg_', 'uk_', 'usa_']
    colnames = ['author', 'text']
    usecols_list = [2, 10]

    entities = ['China', 'US', 'Trump', 'Wuhan']
