import helpers
import os

class Action( object ):
    def __init__( self, platform, configuration, path_resolver, defines_helper, args ):
        self.platform = platform
        self.configuration = configuration
        self.path_resolver = path_resolver
        self.defines_helper = defines_helper
        self.args = args

    def GetUATParameters( self ):
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
    
    def GetBuildCookRunArguments( self ):
        return ""

    def ValidateParameters( self ):
        if self.args.deploy and not self.args.deploy_device:
            raise Exception( "You must specify a device to deploy your game on when you pass the --deploy argument" )

    def Execute( self ):
        parameters = [ "BuildCookRun" ]
        parameters.extend( self.GetUATParameters() )
        parameters.extend( self.GetBuildCookRunArguments() )
        uat = self.path_resolver.GetRunUATPath()

        helpers.StartProcess( uat, parameters )

class ActionBuildEditor( Action ):
    def Execute( self ):
        unreal_build_tool = self.path_resolver.GetUnrealBuildToolPath()
        parameters = [ self.args.project_name + "Editor", self.args.platform, self.args.configuration, self.path_resolver.GetProjectPath() ]
        helpers.StartProcess( unreal_build_tool, parameters )

class ActionBuild( Action ):
    def GetBuildCookRunArguments( self ):
        return [ "-build", "-skipcook" ]

class ActionCook( Action ):
    def GetBuildCookRunArguments( self ):
        arguments = [
            self.configuration.CookArguments,
            "-allmaps",
            "-cook",
            "-unversionedcookedcontent",
            "-package",
        ]

        if self.platform.CanCompressData:
            arguments.append( "-compressed" )
        
        return arguments

class ActionBuildCook( ActionCook ):
    def GetBuildCookRunArguments( self ):
        arguments = super().GetBuildCookRunArguments()
        arguments.append( "-build" )
        return arguments

class ActionBuildCookArchive( ActionBuildCook ):
    def GetBuildCookRunArguments( self ):
        arguments = super().GetBuildCookRunArguments()
        arguments.extend( [ 
            "-stage", 
            "-archive", 
            "-archivedirectory=" + self.GetArchiveDirectory()
        ] )

        return arguments

    def GetArchiveDirectory( self ):
        return self.path_resolver.GetArchiveDirectory()

class ActionPatch( ActionBuildCookArchive ):
    def GetBuildCookRunArguments( self ):
        arguments = super().GetBuildCookRunArguments()

        arguments.extend( [
            "-generatepatch",
            "-basedonreleaseversion=" + self.args.patch_base_version_number,
            "-basedonreleaseversionroot=" + os.path.join( self.args.archive_directory_root, self.args.configuration )
        ] )

        return arguments

    def ValidateParameters( self ):
        super().ValidateParameters()

        if not self.platform.CanBePatched:
            raise Exception ( "The selected platform " + self.platform.Name + " does not allow patches" )
        if self.args.configuration != "Shipping":
            raise Exception( "You must build for the configuration 'Shipping' to patch" )
        if not self.args.patch_base_version_number:
            raise Exception ( "You must provide a patch base version number when packaging a patch" )

class ActionFactory( object ):
    @staticmethod
    def CreateAction( action_name, platform, configuration, path_resolver, defines_helper, args ):
        if action_name == 'BuildEditor':
            return ActionBuildEditor( platform, configuration, path_resolver, defines_helper, args )
        if action_name == 'Build':
            return ActionBuild( platform, configuration, path_resolver, defines_helper, args )
        elif action_name == 'Cook':
            return ActionCook( platform, configuration, path_resolver, defines_helper, args )
        elif action_name == 'BuildCook':
            return ActionBuildCook( platform, configuration, path_resolver, defines_helper, args )
        elif action_name == 'BuildCookArchive':
            return ActionBuildCookArchive( platform, configuration, path_resolver, defines_helper, args )
        elif action_name == 'Patch':
            return ActionPatch( platform, configuration, path_resolver, defines_helper, args )