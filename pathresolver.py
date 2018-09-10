import os
import re

class PathResolver( object ):
    def __init__( self, args ):
        self.args = args

    def GetArchiveDirectory( self ):
        return os.path.join( self.args.archive_directory_root, self.args.configuration, self.args.version_number )

    def GetProjectPath( self ):
        return os.path.join( self.args.project_dir, self.args.project_name + ".uproject" )

    def GetConfigFolderPath( self ):
        return os.path.join( self.args.project_dir, "Config" )

    def GetBuildFolderPath( self ):
        return os.path.join( self.args.project_dir, "Build" )

    def GetRunUATPath( self ):
        return os.path.join( self.args.ue_root_folder, "Engine\\Build\\BatchFiles\\RunUAT.bat" )

    def GetUnrealBuildToolPath( self ):
        return os.path.join( self.args.ue_root_folder, "Engine\\Binaries\\DotNET\\UnrealBuildTool.exe" )