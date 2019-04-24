import subprocess
import globals

def StartProcess( path, arguments ):
    if globals.STUB:
        print( path )
        print( arguments )
    else:
        arguments.insert( 0, path )
        print( "StartProcess : " + " ".join( arguments ) )
        return subprocess.run( arguments, shell=False ).returncode

def PrintError( error_message ):
    print()
    print()
    print( f"ERROR : {error_message}" )
    print()
    print()

def PrintErrorAndQuit( error_message ):
    PrintError( error_message )
    quit()

def PrintIsolatedMessage( message ):
    print()
    print( message )
    print()

def WriteContentToFile( file_path, content ):
    if globals.STUB:
        print( "Would write \r\n{0} \r\nin \r\n{1}".format( content, file_path ) )
    else:
        f = open( file_path, "w+" )
        f.write( content )
        f.close()