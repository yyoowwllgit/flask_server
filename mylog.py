import logging
logging.basicConfig(level=logging.DEBUG,\
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s pid:%(process)s %(message)s',\
    datefmt='%Y-%m-%d %H:%M:%S',\
    filename='selfdef.log',\
    filemode='a')
console=logging.StreamHandler()
console.setLevel(logging.DEBUG)
#formatter=logging.Formatter('%(name)-12s:%(levelname)-8s %(message)s')
formatter=logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s pid:%(process)s %(message)s',\
    '%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
if __name__ == '__main__':
    logging.debug('this is debug')
    logging.info('this is info')
    logging.warning('this is warning')
    logging.error('this is error')
