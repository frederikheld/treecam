"""
Not a real test suite yet!
"""

from modules.data.config import Config

def main():

    config = Config()
    config.loadConfigFromJSONFile('config.json')

    globalConfig = config.getGlobalConfig()
    print(globalConfig.getConfigDict())
    print(globalConfig.getValue('filename_time_format'))

    moduleConfigFTPSUpload = config.getModuleConfig('ftps_upload')
    print(moduleConfigFTPSUpload.getConfigDict())

    print(moduleConfigFTPSUpload.getValue('filename_time_format'))

main()