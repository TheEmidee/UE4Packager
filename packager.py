import configargparse
import configparser
import sys

import globals
import platform
import configuration
import action
import pathresolver
import platformregionhelper
import defineshelper
import functioncaller
import configurationoverride
import helpers
import host

parser = configargparse.ArgParser( ignore_unknown_config_file_keys=True )
parser.add( 'actions', action="store" )
parser.add( 'platform', action="store" )
parser.add( 'configuration', action="store", choices=[ "Development", "Debug", "Shipping" ] )
parser.add( '-c', '--config', required=True, is_config_file=True, help='config file path')
parser.add( '--stub', action="store_true", dest="stub" )
parser.add( "--ue_root_folder", action="store", dest="ue_root_folder", default="" )
parser.add( "--project_dir", action="store", dest="project_dir", default="" )
parser.add( "--project_name", action="store", dest="project_name", default="" )
parser.add( "--archive_directory_root", action="store", dest="archive_directory_root", default="" )
parser.add( "--region", action="store", dest="region", default="" )
parser.add( "--backup_version", action="store_true", dest="backup_version" )
parser.add( "--no_backup_version", action="store_true", dest="no_backup_version", help='Force disable backup. Useful if you enabled backup in the config.ini but want to disable it locally' )
parser.add( "--backup_directory_root", action="store", dest="backup_directory_root", default="" )
parser.add( "--version_number", action="store", dest="version_number", default="" )
parser.add( "--base_version_number", action="store", dest="base_version_number", default="" )
parser.add( "--dlc_name", action="store", dest="dlc_name", default="" )
parser.add( "--compile_automation_scripts", action="store_true", dest="compile_automation_scripts" )
parser.add( "--no_compile_game_editor", action="store_true", dest="no_compile_game_editor" )
parser.add( "--no_iterative_cooking", action="store_true", dest="no_iterative_cooking" )
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

host = host.HostFactory.CreateHost()
configuration_override = configurationoverride.ConfigurationOverride( args, config )

function_caller = functioncaller.FunctionCaller( args )
function_caller.CallCustomInitialize( args, config )

defines_helper = defineshelper.DefinesHelper( config, args )

if args.no_backup_version:
    args.backup_version = False
    helpers.PrintIsolatedMessage( "Force NO Backup" )

try:
    platform_region_helper = platformregionhelper.PlatformRegionHelper( config, args )
    path_resolver = pathresolver.PathResolver( args, host )

    platform = platform.PlatformFactory.CreatePlatform( args.platform, platform_region_helper, host )

    configuration = configuration.ConfigurationFactory.CreateConfiguration( args.configuration )
    configuration.ValidateParameters( args )

    action = action.Action( args.actions, platform, configuration, path_resolver, defines_helper, args, host )
    action.ValidateParameters()
except Exception as e:
    helpers.PrintErrorAndQuit( str( e ) )

exit_code = 0

try:
    platform.PreExecute( args, path_resolver )
    function_caller.CallCustomPreExecute( args, path_resolver )

    exit_code = action.Execute()

    platform.PostExecute( args, path_resolver )
    function_caller.CallCustomPostExecute( args, path_resolver )
    
except Exception as e:
    helpers.PrintError( str( e ) )

sys.exit( exit_code )