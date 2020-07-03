class Config:
    # filepath = os.path.abspath(pkg_resources.resource_filename('__main__', '/MultitextAnalysis/'))
    filepath = '/Users/geminiwenxu/PycharmProjects/MultitextAnalysis/'
    data_path = filepath + 'Data/'
    reports_path = data_path + 'reports/'
    translation_path = data_path + 'translation/'
    keywords = ['covid-19', 'corona', 'coronavirus', 'socialdistance', 'socialdistancing', 'globalpandemic',
                'stayathome', 'FightCOVID19', 'covid', 'outbreak', 'crisis', 'virus', '#conronavirus', '#covid',
                'Coronavirus', 'Covid-19', 'Corona', "#COVID19", '#coronavirus']
    country_prefix = ['de_', 'fr_', 'jp_', 'kr_', 'nl_', 'sg_', 'uk_', 'usa_', 'aus_', 'cn_']
    colnames = ['author', 'text']
    usecols_list = [2, 10]

    entities = ['China', 'US', 'Trump', 'Wuhan']

    test_prefix = ['test_']
