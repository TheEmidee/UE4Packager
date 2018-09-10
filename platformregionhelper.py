import json

class PlatformRegionHelper( object ):

    TitleId = ""
    Region = ""
    DefaultTitleId = ""

    def __init__( self, config, args ):
        region_section = "REGIONS"

        if not config.has_section( region_section ):
            print( "No REGIONS section exists in the config file" )
            return

        option_key = args.platform + "Regions"
        if not config.has_option( region_section, option_key ):
            print( f"No option {option_key} in the section '{region_section}'" )
            return

        default_region_key = args.platform + "DefaultRegion"
        if not config.has_option( region_section, default_region_key ):
            raise Exception( "There is no '" + default_region_key + "' key in the section '" + region_section + "'" )

        regions = json.loads( config.get( region_section, option_key ) )

        default_region = config.get( region_section, default_region_key )
        if not default_region in regions:
            raise Exception( "The default region '" + default_region + "' is not in the region list" )

        self.Region = args.region
        
        if not self.Region:
            print( f"No region argument passed. Use default region : '{default_region}'" )
            self.Region = default_region
        
        if not self.Region in regions:
            raise Exception( "The region '" + self.Region + "' was not found in the section '" + region_section + "' for the key '" + option_key + "'" )

        self.TitleId = self.__GetTitleIdForRegion( config, args, self.Region, True )
        self.DefaultTitleId = self.__GetTitleIdForRegion( config, args, default_region, False )

    def __GetTitleIdForRegion( self, config, args, region, use_build_option ):
        title_id = ""

        if use_build_option:
            platform_region_key = f"{args.platform}Region_{args.build_option}_{region}"
            title_id = self.__TryGetRegionTitleId( config, platform_region_key )

        if not title_id:
            platform_region_key = args.platform + "Region_" + region
            title_id = self.__TryGetRegionTitleId( config, platform_region_key )
            if not title_id:
                raise Exception( f"Unable to found the option {platform_region_key} in the section 'REGIONS'" )

        return title_id

    def __TryGetRegionTitleId( self, config, key ):
        value = ""
        if config.has_option( 'REGIONS', key ):
            value = config.get( "REGIONS", key )
        return value