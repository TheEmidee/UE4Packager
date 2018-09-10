import inspect
import importlib
import importlib.util
import sys
import os

class FunctionCaller( object ):
    def __init__( self, args ):
        self.modules = []

        if not args.custom_folder:
            return

        custom_functions_path = args.custom_folder
        files = os.listdir( args.custom_folder )

        for file_to_include in files:
            if not file_to_include.endswith( ".py" ):
                continue

            file_no_ext = os.path.splitext( file_to_include )[0]
            module = self.__ModuleFromFile( file_no_ext, os.path.join( args.custom_folder, file_to_include ) )

            if not module:
                continue

            self.modules.append( module )

    def CallCustomInitialize( self, args, config ):
        self.__CallAllFunctionDefinitions( "Initialize", args, config )

    def CallCustomPreExecute( self, args, path_resolver ):
        self.__CallAllFunctionDefinitions( "PreExecute", args, path_resolver )

    def CallCustomPostExecute( self, args, path_resolver ):
        self.__CallAllFunctionDefinitions( "PostExecute", args, path_resolver )

    def __ModuleFromFile( self, module_name, file_path ):
        spec = importlib.util.spec_from_file_location( module_name, file_path )
        if not spec:
            return None

        module = importlib.util.module_from_spec( spec )
        spec.loader.exec_module( module )
        return module

    def __CallAllFunctionDefinitions( self, function_name, args, *argv ):
        self.__TryCallFunction( f"Custom_{args.build_option}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.platform}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.configuration}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.build_option}_{args.platform}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.build_option}_{args.configuration}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.platform}_{args.configuration}_{function_name}", args, *argv )
        self.__TryCallFunction( f"Custom_{args.build_option}_{args.platform}_{args.configuration}_{function_name}", args, *argv )

    def __TryCallFunction( self, function_name, args, *argv ):
        for module in self.modules:
            if hasattr( module, function_name ):
                print( f"Call function '{function_name}' from included file '{module.__name__}'" )
                getattr( module, function_name )( args, *argv )