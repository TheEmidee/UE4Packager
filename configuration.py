class Configuration( object ):
    def __init__( self ):
        self.CookArguments = ""

    def ValidateParameters( self, args ):
        pass

class ConfigurationDebug( Configuration ):
    def __init__( self ):
        self.CookArguments = "-iterativecooking"

class ConfigurationDevelopment( Configuration ):
    def __init__( self ):
        self.CookArguments = "-iterativecooking"

class ConfigurationShipping( Configuration ):
    def __init__( self ):
        self.CookArguments = "-distribution"
    
    # def ValidateParameters( self, args ):
    #     if not args.action in [ "BuildCookArchive", "Patch" ]:
    #         raise Exception ( "You must use 'BuildCookArchive' or 'Patch' in 'Shipping'" )
    #     if not args.version_number:
    #         raise Exception ( "You must provide a version_number when using the 'Shipping' configuration" )

class ConfigurationFactory( object ):
    @staticmethod
    def CreateConfiguration( configuration_name ):
        if configuration_name == 'Debug':
            return ConfigurationDebug()
        elif configuration_name == 'Development':
            return ConfigurationDevelopment()
        elif configuration_name == 'Shipping':
            return ConfigurationShipping()