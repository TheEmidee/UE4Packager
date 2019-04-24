from sys import platform
from shutil import copyfile
import helpers
import subprocess

class Host( object ):
    def GetRunUATPath( self ):
        return ""
    def GetUnrealBuildToolPath( self ):
        return ""
    def GetCopyExecutable( self ):
        return ""
    def GetCopyFilesArguments( self ):
        return []
    def GetCopyDirectoriesArguments( self ):
        return []
    def CopyFile( self, source, destination ):
        print( "Copy file from " + source + " to " + destination )
        copyfile( source, destination )
    def CopyDirectories( self, source, destination ):
        print( "Copy directories from " + source + " to " + destination )
        arguments = [ source, destination ]
        arguments.extend( self.GetCopyDirectoriesArguments() )
        return helpers.StartProcess( self.GetCopyExecutable(), arguments )

class HostLinux( Host ):
    def GetRunUATPath( self ):
        return "Engine/Build/BatchFiles/RunUAT.sh"
    def GetUnrealBuildToolPath( self ):
        return "Engine/Binaries/Linux/UnrealBuildTool"
    def GetCopyExecutable( self ):
        return "cp"
    def GetCopyFilesArguments( self ):
        return []
    def GetCopyDirectoriesArguments( self ):
        return []

class HostWindows( Host ):
    def GetRunUATPath( self ):
        return "Engine\\Build\\BatchFiles\\RunUAT.bat"
    def GetUnrealBuildToolPath( self ):
        return "Engine\\Binaries\\DotNET\\UnrealBuildTool.exe"
    def GetCopyExecutable( self ):
        return "robocopy"
    def GetCopyFilesArguments( self ):
        return [ "/FFT", "/R:3", "/W:10", "/Z", "/NP" ]
    def GetCopyDirectoriesArguments( self ):
        return [ "/E", "/FFT", "/R:3", "/W:10", "/Z", "/NP", "/NDL" ]
    def CopyDirectories( self, source, destination ):
        print( "Copy directories from " + source + " to " + destination )
        arguments = [ source, destination ]
        arguments.extend( self.GetCopyDirectoriesArguments() )
        try:
            return helpers.StartProcess( self.GetCopyExecutable(), arguments )
        except subprocess.CalledProcessError as e:
            if not self.__ProcessReturnCode( e.returncode ):
                raise e

    def __ProcessReturnCode( self, return_code ):
        switcher = {
            16 : { "message" : "***FATAL ERROR***", "success" : "false" },
            15 : { "message" : "OKCOPY + FAIL + MISMATCHES + XTRA", "success" : "false" },
            14 : { "message" : "FAIL + MISMATCHES + XTRA", "success" : "false" },
            13 : { "message" : "OKCOPY + FAIL + MISMATCHES", "success" : "false" },
            12 : { "message" : "FAIL + MISMATCHE", "success" : "false" },
            11 : { "message" : "OKCOPY + FAIL + XTRA", "success" : "false" },
            10 : { "message" : "FAIL + XTRA", "success" : "false" },
            9 : { "message" : "OKCOPY + FAIL", "success" : "false" },
            8 : { "message" : "FAIL", "success" : "false" },
            7 : { "message" : "OKCOPY + MISMATCHES + XTRA", "success" : "true" },
            6 : { "message" : "MISMATCHES + XTRA", "success" : "true" },
            5 : { "message" : "OKCOPY + MISMATCHES", "success" : "true" },
            4 : { "message" : "MISMATCHES", "success" : "true" },
            3 : { "message" : "OKCOPY + XTRA", "success" : "true" },
            2 : { "message" : "XTRA", "success" : "true" },
            1 : { "message" : "OKCOPY", "success" : "true" },
            0 : { "message" : "No Change", "success" : "true" }
        }

        value = switcher.get( return_code )
        helpers.PrintIsolatedMessage( value[ "message"] )
        return value[ "success" ] == "true"

class HostOSX( Host ):
    def GetRunUATPath( self ):
        return "Engine/Build/BatchFiles/RunUAT.sh"
    def GetUnrealBuildToolPath( self ):
        return "Engine/Binaries/Linux/UnrealBuildTool"
    def GetCopyExecutable( self ):
        return "cp"
    def GetCopyFilesArguments( self ):
        return []
    def GetCopyDirectoriesArguments( self ):
        return []

class HostFactory( object ):
    @staticmethod
    def CreateHost():
        if platform == "linux" or platform == "linux2":
            return HostLinux()
        elif platform == 'win32' or platform == "cygwin":
            return HostWindows()
        elif platform == "darwin":
            return HostOSX()