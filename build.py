from __future__ import annotations
from typing import Final as const
import subprocess


class BuildParamInterface():
    """_summary_\n
    ビルドに使用するパラメーター
    """
    
    def __init__(self, target:str, no_console: bool = True,icon: str|None = None, binarys: list[str]|None = None, compile_one_file:bool|None=False, hidden_import:list[str]|None=None) -> None:
        self.TARGET_FILE:str = target
        self.ICON_PATH:str|None = icon
        self.BINARYS:list[str]|None = binarys
        self.DO_ONEFILE:bool|None = compile_one_file
        self.HIDDEN_IMPORTS:list[str]|None = hidden_import
        self.NO_CONSOLE:bool = no_console
        


class AppBuild():
    """_summary_\n
    コマンドを実行しアプリケーションのビルドを行う
    """
    
    BUILDER: const[str] = "pyinstaller"
    BUILDABLE: const[list[str]] = [
        ".py"
        ".spec"
    ]
    
    def __init__(self, param:BuildParamInterface) -> None:
        self.param = param
        self.output = self.__get_output_dir()
        
    def __binary_build(self) -> None:
        """_summary_\n
        .py -> .exeの変換を行う。
        """
        command:str = self.BUILDER + " " + self.param.TARGET_FILE
        if self.param.ICON_PATH is not None:
            command += " --icon=" + self.param.ICON_PATH
        if self.param.DO_ONEFILE is True:
            command += " --onefile"
        if self.param.NO_CONSOLE:
            command += " --noconsole"
        if self.param.HIDDEN_IMPORTS is not None:
            for module in self.param.HIDDEN_IMPORTS:
                command += " --hidden-import " + module + " "
        
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as err:
            print(err)
            
    
    def __copy_binary(self, binary:str, target:str) -> None:
        """_summary_\n
        バイナリファイルをdistにコピーする
        """
        command:const[str] = "cp -r -v " + binary + " " + target

        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as err:
            print(err)
    
    
    def build(self):
        """_summary_\n
        ビルドを実行する。
        """
        self.__binary_build()
        
        if self.param.BINARYS is not None:
            for path in self.param.BINARYS:
                self.__copy_binary(path, self.output)
        if self.param.ICON_PATH is not None:
            self.__copy_binary(self.param.ICON_PATH, self.output)
            
        print("Build Complete!")
        print("Output: " + self.output)
        
    
    
    def __get_output_dir(self) -> str:
        """_summary_\n
        ファイル名を取得する（拡張子の除く純粋なファイル名文字列）
        ※Pyinstallerはファイル名フォルダ直下にexeを生成するため。
        """
        filename:str = self.param.TARGET_FILE.split("/")[-1].replace(".py", "")
        return "dist/" + filename







if __name__ == "__main__":
    ### 以下のゾーンにビルドパラメーターを入力して実行してください。
    
    buildParam = BuildParamInterface(
        "main.py",
        no_console=False,
        icon="e6832bee44cfe3a3844f0a2587ee4bc4_xxo.ico",
        binarys=[
            "chrome-win",
            "chromedriver_win32"
            ],
        compile_one_file=False,
        hidden_import=[]
    )
    
    AppBuild(buildParam).build()