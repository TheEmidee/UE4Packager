class ConfigurationOverride( object ):
    def __init__( self, args, config ):
        self.config = config
        self.args = args
        self.section_name = "CONFIG_OVERRIDES"
        self.updated_values = {}

        if not self.config.has_section( self.section_name ):
            print( f"No {self.section_name} section found in the ini file" )
            return

        for argument, value in args.__dict__.items():
            self.__TryOverrideArgument( f"{args.build_option}", argument )
            self.__TryOverrideArgument( f"{args.platform}", argument )
            self.__TryOverrideArgument( f"{args.configuration}", argument )
            self.__TryOverrideArgument( f"{args.build_option}_{args.platform}", argument )
            self.__TryOverrideArgument( f"{args.build_option}_{args.configuration}", argument )
            self.__TryOverrideArgument( f"{args.platform}_{args.configuration}", argument )
            self.__TryOverrideArgument( f"{args.build_option}_{args.platform}_{args.configuration}", argument )

        for argument, value in self.updated_values.items():
            setattr( self.args, argument, value )

    def __TryOverrideArgument( self, config_key_prefix, argument ):
        option_key = f"{config_key_prefix}_{argument}"
        if self.config.has_option( self.section_name, option_key ):
            new_value = self.config.get( self.section_name, option_key )
            self.updated_values[ argument ] = new_value
