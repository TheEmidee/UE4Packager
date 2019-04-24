import helpers
import os

class Action( object ):
    def __init__( self, actions, platform, configuration, path_resolver, defines_helper, args, host ):
        self.actions = actions.split( '+' )
        self.platform = platform
        self.configuration = configuration
        self.path_resolver = path_resolver
        self.defines_helper = defines_helper
        self.args = args
        self.host = host
        self.allowed_actions = [ "Build", "Cook", "Archive" ]
        self.unique_actions = [ "Patch", "BuildEditor", "Release", "DLC" ]

    def ValidateParameters( self ):
        if len( self.actions ) > 1:
            for i in range ( 0, len( self.actions ) ) :
                if self.actions[i] in self.unique_actions:
                        raise Exception( "The action : {0} can be the only action".format( self.actions[i] ) )

        for i in range ( 0, len( self.actions ) ) :
            if self.actions[i] not in self.allowed_actions and self.actions[i] not in self.unique_actions:
                raise Exception( "Invalid action : {0}".format( self.actions[i] ) )

        if "Release" in self.actions:
            if not self.args.version_number:
                raise Exception( "You must provide a version_number to Release" )

        if "Patch" in self.actions:
            if not self.platform.CanBePatched:
                raise Exception ( "The selected platform " + self.platform.Name + " does not allow patches" )
            if not self.args.base_version_number:
                raise Exception ( "You must provide a patch base version number when creating a patch" )

        if "DLC" in self.actions:
            if not self.args.base_version_number:
                raise Exception ( "You must provide a base version number when creating a DLC" )
            if not self.args.dlc_name:
                raise Exception ( "You must provide a DLC name when creating a DLC" )

        if len( self.actions ) == 1 and self.actions[ 0 ] in self.unique_actions:
            self.actions.extend( [ "Build", "Cook", "Archive" ] )

        if self.args.deploy and not self.args.deploy_device:
            raise Exception( "You must specify a device to deploy your game on when you pass the --deploy argument" )

        if self.args.backup_version and not "Archive" in self.actions:
            raise Exception( "You must choose to archive the project in order to backup the version" )

        if self.args.backup_version and not self.args.backup_directory_root:
            raise Exception( "The parameter backup_directory_root must be set to backup the version" )

    def Execute( self ):
        if "BuildEditor" in self.actions:
            return self.__BuildEditor()
        else:
            return self.__BuildCookRun()

    def __BuildEditor( self ):
        unreal_build_tool = self.path_resolver.GetUnrealBuildToolPath()
        parameters = [ self.args.project_name + "Editor", self.args.platform, self.args.configuration, self.path_resolver.GetProjectPath() ]
        return helpers.StartProcess( unreal_build_tool, parameters )

    def __BuildCookRun( self ):
        parameters = [ "BuildCookRun" ]
        parameters.extend( self.__GetUATParameters() )
        parameters.extend( self.__GetBuildCookRunArguments() )
        uat = self.path_resolver.GetRunUATPath()

        exit_code = helpers.StartProcess( uat, parameters )

        if self.args.backup_version:
            self.__BackupVersion()

        return exit_code

    def __BackupVersion( self ):
        helpers.PrintIsolatedMessage( "Backup version" )

        source = os.path.join( 
            self.path_resolver.GetArchiveDirectory(),
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId
            )
        destination = os.path.join( 
            self.args.backup_directory_root, 
            self.args.project_name,
            self.args.configuration, 
            self.args.version_number
            )

        if self.args.build_option:
            destination = os.path.join( destination, self.args.build_option )

        destination = os.path.join(
            destination,
            self.platform.GetPackagedFolderName(),
            self.platform.TitleId 
            )

        self.__BackupFolder( source, destination )

        if "Release" in self.actions:
            helpers.PrintIsolatedMessage( "Backup Releases Folder" )

            source = os.path.join( 
                self.args.project_dir,
                "Releases",
                self.args.version_number,
                self.platform.GetPackagedFolderName(),
                self.platform.TitleId
                )
            destination = os.path.join( 
                self.args.backup_directory_root, 
                self.args.project_name,
                "Releases",
                self.args.version_number,
                self.platform.GetPackagedFolderName(),
                self.platform.TitleId
                )
                
            self.__BackupFolder( source, destination )

    def __BackupFolder( self, source, destination ):
        self.host.CopyDirectories( source, destination )

    def __GetUATParameters( self ):
        result = [
            "-project=" + self.path_resolver.GetProjectPath(),
            "-noP4",
            "-clientconfig=" + self.args.configuration,
            "-utf8output",
            "-platform=" + self.args.platform
        ]
        
        if self.args.compile_automation_scripts:
            result.append( "-compile" )
        else:
            result.append( "-nocompile" )

        if self.args.no_compile_game_editor:
            result.append( "-nocompileeditor" )

        if self.platform.TitleId:
            result.append( "-titleid=" + self.platform.TitleId )

        result.extend( self.defines_helper.DefinesArguments )

        if self.args.deploy:
            result.extend( [ "-deploy", f"-device={self.args.deploy_device}" ] )

        # Use the following arguments on a build server ???
        # $result += " -installed -ue4exe=UE4Editor-Cmd.exe"

        return result

    def __GetBuildCookRunArguments( self ):
        arguments = []

        if "Build" in self.actions:
            arguments.append( "-build" )

        if "Cook" not in self.actions:
            arguments.append( "-skipcook" )
        else:
            arguments.extend( [
                "-allmaps",
                "-cook",
                #"-unversionedcookedcontent",
                "-package"
            ] )

            if any( a in [ "Release", "Patch" ] for a in self.actions ):
                arguments.append( "-distribution" )
                arguments.append( "-createreleaseversion=" + self.args.version_number )
            elif not self.args.no_iterative_cooking:
                arguments.append( "-iterativecooking" )

            if "Archive" in self.actions:
                arguments.append( "-pak" )

            if self.platform.CanCompressData:
                arguments.append( "-compressed" )

        if "Archive" in self.actions:
            arguments.extend( [ 
                "-stage", 
                "-archive", 
                "-archivedirectory=" + self.path_resolver.GetArchiveDirectory()
            ] )

        if "Patch" in self.actions:
            arguments.extend( [
                "-generatepatch",
                "-basedonreleaseversion=" + self.args.base_version_number,
                "-basedonreleaseversionroot=" + os.path.join( self.args.archive_directory_root, self.args.configuration )
            ] )

        if "DLC" in self.actions:
            arguments.extend([
                "-dlcname=" + self.args.dlc_name,
                "-basedonreleaseversion=" + self.args.base_version_number
            ])

        return arguments