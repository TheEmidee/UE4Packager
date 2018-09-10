import configargparse
import configparser
import sys

import globals
import platform
import configuration
import action
import backup
import pathresolver
import platformregionhelper
import defineshelper
import functioncaller
import configurationoverride
import helpers

parser = configargparse.ArgParser( ignore_unknown_config_file_keys=True )
parser.add( 'action', action="store", choices=[ "BuildEditor", "Build", "Cook", "BuildCook", "BuildCookArchive", "Patch" ] )
parser.add( 'platform', action="store", choices=[ "Win64", "XboxOne", "PS4", "Switch" ] )
parser.add( 'configuration', action="store", choices=[ "Development", "Debug", "Shipping" ] )
parser.add( '-c', '--config', required=True, is_config_file=True, help='config file path')
parser.add( '--stub', action="store_true", dest="stub" )
parser.add( "--ue_root_folder", action="store", dest="ue_root_folder", default="" )
parser.add( "--project_dir", action="store", dest="project_dir", default="" )
parser.add( "--project_name", action="store", dest="project_name", default="" )
parser.add( "--archive_directory_root", action="store", dest="archive_directory_root", default="" )
parser.add( "--region", action="store", dest="region", default="" )
parser.add( "--backup_version", action="store_true", dest="backup_version" )
parser.add( "--backup_directory_root", action="store", dest="backup_directory_root", default="" )
parser.add( "--version_number", action="store", dest="version_number", default="" )
parser.add( "--patch_base_version_number", action="store", dest="patch_base_version_number", default="" )
parser.add( "--compile_automation_scripts", action="store_true", dest="compile_automation_scripts" )
parser.add( "--no_compile_game_editor", action="store_true", dest="no_compile_game_editor" )
parser.add( "--custom_folder", action="store", dest="custom_folder" )
parser.add( "--build_option", action="store", dest="build_option" )
parser.add( "--deploy", action="store_true", dest="deploy" )
parser.add( "--deploy_device", action="store", dest="deploy_device" )

args = parser.parse_args()

globals.STUB = args.stub

if globals.STUB:
    print()
    print( "******************" )
    print( "*****  STUB  *****" )
    print( "******************" )
    print()

config = configparser.ConfigParser()
config.read( args.config )

configuration_override = configurationoverride.ConfigurationOverride( args, config )

function_caller = functioncaller.FunctionCaller( args )
function_caller.CallCustomInitialize( args, config )

defines_helper = defineshelper.DefinesHelper( config, args )

try:
    platform_region_helper = platformregionhelper.PlatformRegionHelper( config, args )
    path_resolver = pathresolver.PathResolver( args )

    platform = platform.PlatformFactory.CreatePlatform( args.platform, platform_region_helper )

    configuration = configuration.ConfigurationFactory.CreateConfiguration( args.configuration )
    configuration.ValidateParameters( args )

    action = action.ActionFactory.CreateAction( args.action, platform, configuration, path_resolver, defines_helper, args )
    action.ValidateParameters()

    backup = backup.Backup( args, path_resolver, platform )
    backup.ValidateParameters()

except Exception as e:
    helpers.PrintErrorAndQuit( str( e ) )

try:
    platform.PreExecute( args, path_resolver )
    function_caller.CallCustomPreExecute( args, path_resolver )

    action.Execute()

    if args.backup_version:
        backup.BackupVersion()

except Exception as e:
    helpers.PrintError( str( e ) )

platform.PostExecute( args, path_resolver )
function_caller.CallCustomPostExecute( args, path_resolver )