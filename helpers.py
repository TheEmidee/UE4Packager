import subprocess
import globals

def StartProcess( path, arguments ):
    if globals.STUB:
        print( path )
        print( arguments )
    else:
        arguments.insert( 0, path )
        subprocess.check_call( arguments, shell=False )

def PrintError( error_message ):
    print()
    print()
    print( f"ERROR : {error_message}" )
    print()
    print()

def PrintErrorAndQuit( error_message ):
    PrintError( error_message )
    quit()