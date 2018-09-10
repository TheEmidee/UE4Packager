import json

class DefinesHelper( object ):
    DefinesArguments = []

    def __init__( self, config, args ):

        self.config = config
        self.args = args
        self.defines_section = "DEFINES"

        if not self.config.has_section( self.defines_section ):
            print( "No DEFINES section found in the ini file" )
            return

        self.__TryAddDefineForOption( f"Defines_{args.build_option}" )
        self.__TryAddDefineForOption( f"Defines_{args.platform}" )
        self.__TryAddDefineForOption( f"Defines_{args.configuration}" )
        self.__TryAddDefineForOption( f"Defines_{args.build_option}_{args.platform}" )
        self.__TryAddDefineForOption( f"Defines_{args.build_option}_{args.configuration}" )
        self.__TryAddDefineForOption( f"Defines_{args.platform}_{args.configuration}" )
        self.__TryAddDefineForOption( f"Defines_{args.build_option}_{args.platform}_{args.configuration}" )

    def __TryAddDefineForOption( self, option_key ):
        if self.config.has_option( self.defines_section, option_key ):
            defines = json.loads( self.config.get( self.defines_section, option_key ) )
            self.DefinesArguments.extend( defines )