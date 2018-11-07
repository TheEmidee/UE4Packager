import helpers
import os

class Action( object ):
    def __init__( self, actions, platform, configuration, path_resolver, defines_helper, args ):
        self.actions = actions.split( '+' )
        self.platform = platform
        self.configuration = configuration
        self.path_resolver = path_resolver
        self.defines_helper = defines_helper
        self.args = args
        self.allowed_actions = [ "Build", "Cook", "Archive", "Patch", "BuildEditor" ]

    def ValidateParameters( self ):
        for i in range ( 0, len( self.actions ) ) :
            if self.actions[i] not in self.allowed_actions:
                raise Exception( "Invalid action : {0}".format( self.actions[i] ) )

        if "BuildEditor" in self.actions:
            if len( self.actions ) > 1:
                raise Exception( "BuildEditor can be the only action" )

        if "Patch" in self.actions:
            if not self.platform.CanBePatched:
                raise Exception ( "The selected platform " + self.platform.Name + " does not allow patches" )
            if self.args.configuration != "Shipping":
                raise Exception( "You must build for the configuration 'Shipping' to patch" )
            if not self.args.patch_base_version_number:
                raise Exception ( "You must provide a patch base version number when packaging a patch" )

        if self.args.deploy and not self.args.deploy_device:
            raise Exception( "You must specify a device to deploy your game on when you pass the --deploy argument" )

    def Execute( self ):
        if "BuildEditor" in self.actions:
            self.__BuildEditor()
        else:
            self.__BuildCookRun()

    def __BuildEditor( self ):
        unreal_build_tool = self.path_resolver.GetUnrealBuildToolPath()
        parameters = [ self.args.project_name + "Editor", self.args.platform, self.args.configuration, self.path_resolver.GetProjectPath() ]
        helpers.StartProcess( unreal_build_tool, parameters )

    def __BuildCookRun( self ):
        parameters = [ "BuildCookRun" ]
        parameters.extend( self.__GetUATParameters() )
        parameters.extend( self.__GetBuildCookRunArguments() )
        uat = self.path_resolver.GetRunUATPath()

        helpers.StartProcess( uat, parameters )

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
                    self.configuration.CookArguments,
                    "-allmaps",
                    "-cook",
                    "-unversionedcookedcontent",
                    "-package",
                    "-pak"
            ] )

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
                "-basedonreleaseversion=" + self.args.patch_base_version_number,
                "-basedonreleaseversionroot=" + os.path.join( self.args.archive_directory_root, self.args.configuration )
            ] )

        return arguments