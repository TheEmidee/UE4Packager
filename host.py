from sys import platform
import helpers

class Host( object ):
    def GetRunUATPath( self ):
        return ""
    def GetUnrealBuildToolPath( self ):
        return ""
    def GetCopyExecutable( self ):
        return ""
    def GetCopyArguments( self ):
        return []
    def CopyFiles( self, source, destination ):
        print( "Copy files from " + source + " to " + destination )
        arguments = [ source, destination ]
        arguments.extend( self.GetCopyArguments() )
        helpers.StartProcess( self.GetCopyExecutable(), arguments )

class HostLinux( Host ):
    def GetRunUATPath( self ):
        return "Engine/Build/BatchFiles/RunUAT.sh"
    def GetUnrealBuildToolPath( self ):
        return "Engine/Binaries/Linux/UnrealBuildTool"
    def GetCopyExecutable( self ):
        return "cp"
    def GetCopyArguments( self ):
        return []

class HostWindows( Host ):
    def GetRunUATPath( self ):
        return "Engine\\Build\\BatchFiles\\RunUAT.bat"
    def GetUnrealBuildToolPath( self ):
        return "Engine\\Binaries\\DotNET\\UnrealBuildTool.exe"
    def GetCopyExecutable( self ):
        return "robocopy"
    def GetCopyArguments( self ):
        return [ "/E", "/FFT", "/R:3", "/W:10", "/Z", "/NP", "/NDL" ]

class HostOSX( Host ):
    def GetRunUATPath( self ):
        return "Engine/Build/BatchFiles/RunUAT.sh"
    def GetUnrealBuildToolPath( self ):
        return "Engine/Binaries/Linux/UnrealBuildTool"
    def GetCopyExecutable( self ):
        return "cp"
    def GetCopyArguments( self ):
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