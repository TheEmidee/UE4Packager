import os

import helpers

class Platform( object ):
    CanBePatched = False
    CanCompressData = True
    Name = ""
    TitleId = ""
    
    def __init__( self, platform_region_helper ):
        self.platform_region_helper = platform_region_helper

        self.TitleId = platform_region_helper.TitleId

    def GetPackagedFolderName( self ):
        return self.Name

    def PreExecute( self, args, path_resolver ):
        if self.TitleId:
            print( "Copy TitleId Files" )
            self.__CopyPlatformTitleIdConfig( path_resolver, self.TitleId )

    def PostExecute( self, args, path_resolver ):
        if self.TitleId:
            print( "Restore DefaultTitleId Files" )
            self.__CopyPlatformTitleIdConfig( path_resolver, self.platform_region_helper.DefaultTitleId )

    def GetPlatformBuildFolderPath( self, path_resolver ):
        return os.path.join( path_resolver.GetBuildFolderPath(), self.__GetConfigFolderName() )

    def __CopyPlatformTitleIdConfig( self, path_resolver, title_id ):
        config_dir = self.__GetPlatformConfigFolderPath( path_resolver )
        title_id_config_dir = os.path.join( config_dir, title_id )
        helpers.StartProcess( "xcopy", [ "/y", title_id_config_dir + "\*.*", config_dir ] )

    def __GetPlatformConfigFolderPath( self, path_resolver ):
        return os.path.join( path_resolver.GetConfigFolderPath(), self.__GetConfigFolderName() )

    def __GetConfigFolderName( self ):
        return self.Name

class PlatformWin64( Platform ):
    def __init__( self, platform_region_helper ):
        super( PlatformWin64, self ).__init__( platform_region_helper )
        self.Name = "Win64"

class PlatformPS4( Platform ):
    def __init__( self, platform_region_helper ):
        self.Name = "PS4"
        self.CanBePatched = True
        self.CanCompressData = False

        super( PlatformPS4, self ).__init__( platform_region_helper )

    def PreExecute( self, args, path_resolver ):
        super( PlatformPS4, self ).PreExecute( args, path_resolver )
        
        print( "Copy SceSys Files" )
        self.__CopySceSys( args.project_dir, self.TitleId )        

    def PostExecute( self, args, path_resolver ):
        super( PlatformPS4, self ).PostExecute( args, path_resolver )
        
        print( "Restore SceSys Files" )
        self.__CopySceSys( args.project_dir, self.platform_region_helper.DefaultTitleId ) 

    def __CopySceSys( self, project_dir, title_id ):
        sce_folder_path = os.path.join( project_dir, "Build", "PS4", "sce_sys" )
        title_id_sce_dir = os.path.join( sce_folder_path, title_id )
        helpers.StartProcess( "xcopy", [ "/y", title_id_sce_dir + "\*.*", sce_folder_path ] )

class PlatformXboxOne( Platform ):
    def __init__( self, platform_region_helper ):
        self.Name = "XboxOne"

        super( PlatformXboxOne, self ).__init__( platform_region_helper )

class PlatformSwitch( Platform ):
    def __init__( self, platform_region_helper ):
        self.Name = "Switch"
        self.CanBePatched = True

        super( PlatformSwitch, self ).__init__( platform_region_helper )

    def PreExecute( self, args, path_resolver ):
        super( PlatformSwitch, self ).PreExecute( args, path_resolver )
        
        print( "Copy Resources Files" )
        self.__CopyResources( path_resolver, self.TitleId )        

    def PostExecute( self, args, path_resolver ):
        super( PlatformSwitch, self ).PostExecute( args, path_resolver )
        
        print( "Restore Resources Files" )
        self.__CopyResources( path_resolver, self.platform_region_helper.DefaultTitleId ) 

    def __CopyResources( self, path_resolver, title_id ):
        resources_path = os.path.join( self.GetPlatformBuildFolderPath( path_resolver ), "Resources" )
        title_id_resources_dir = os.path.join( resources_path, title_id )
        helpers.StartProcess( "xcopy", [ "/y", title_id_resources_dir + "\*.*", resources_path ] )

class PlatformFactory( object ):
    @staticmethod
    def CreatePlatform( platform_name, platform_region_helper ):
        if platform_name == 'Win64':
            return PlatformWin64( platform_region_helper )
        elif platform_name == 'PS4':
            return PlatformPS4( platform_region_helper )
        elif platform_name == 'XboxOne':
            return PlatformXboxOne( platform_region_helper )
        elif platform_name == 'Switch':
            return PlatformSwitch( platform_region_helper )