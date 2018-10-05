import os
import helpers

class Backup( object ):
    def __init__( self, args, path_resolver, host, platform ):
        self.args = args
        self.platform = platform
        self.path_resolver = path_resolver
        self.host = host

    def ValidateParameters( self ):
        if self.args.backup_version and not self.args.backup_directory_root:
            raise Exception( "The parameter backup_directory_root must be set to backup the version" )

    def BackupVersion( self ):
        print( "Backup version" )
        
        source = os.path.join( 
            self.path_resolver.GetArchiveDirectory(),
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId
            )
        destination = os.path.join( 
            self.args.backup_directory_root, 
            self.args.project_name,
            self.args.configuration, 
            self.args.version_number,
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId
            )

        self.host.CopyFiles( source, destination )