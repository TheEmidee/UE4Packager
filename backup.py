import os
import helpers

class Backup( object ):
    def __init__( self, args, path_resolver, platform ):
        self.args = args
        self.platform = platform
        self.path_resolver = path_resolver

    def ValidateParameters( self ):
        if self.args.backup_version and not self.args.backup_directory_root:
            raise Exception( "The parameter backup_directory_root must be set to backup the version" )

    def BackupVersion( self ):
        source = os.path.join( 
            self.path_resolver.GetArchiveDirectory(),
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId
            )

        print( "Backup version" )
        print( "From : " + source )

        destination = os.path.join( 
            self.args.backup_directory_root, 
            self.args.project_name,
            self.args.configuration, 
            self.args.version_number,
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId
            )
        
        print( "To : " + destination )

        arguments = [
            source,
            destination,
            "/E",
            "/FFT",
            "/R:3",
            "/W:10",
            "/Z",
            "/NP",
            "/NDL"
        ]

        helpers.StartProcess( "robocopy", arguments )