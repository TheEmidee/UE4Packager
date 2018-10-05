import os
import re

class PathResolver( object ):
    def __init__( self, args, host ):
        self.args = args
        self.host = host

    def GetArchiveDirectory( self ):
        result = os.path.join( self.args.archive_directory_root, self.args.configuration, self.args.version_number )

        if self.args.build_option:
            result = os.path.join( result, self.args.build_option )

        return result

    def GetProjectPath( self ):
        return os.path.join( self.args.project_dir, self.args.project_name + ".uproject" )

    def GetConfigFolderPath( self ):
        return os.path.join( self.args.project_dir, "Config" )

    def GetBuildFolderPath( self ):
        return os.path.join( self.args.project_dir, "Build" )

    def GetRunUATPath( self ):
        return os.path.join( self.args.ue_root_folder, self.host.GetRunUATPath() )

    def GetUnrealBuildToolPath( self ):
        return os.path.join( self.args.ue_root_folder, self.host.GetUnrealBuildToolPath() )