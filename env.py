from os import listdir,chdir
from shutil import move

import os
import dotenv
import logging

class TextFormatter:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   RESET = END = '\033[0m'

class CustomColor:
    def __init__(self,r:int,g:int,b:int):
        self.r = r
        self.g = g
        self.b = b
    
    def rgb(self)->str:
        return f'\u001b[38;2;{self.r};{self.g};{self.b}m'
    
logging.basicConfig(level=logging.INFO,format=TextFormatter.GREEN+"[%(asctime)s][%(levelname)s][ProcID:%(process)d][filename-->%(filename)s line no-->%(lineno)s] >>>>>> "+TextFormatter.RESET+"%(message)s ")

def ls(dir:str)->list[str]:
    try:
        dirs=listdir(dir)
        dir_list=[]
        for dir in dirs:
            dir_list.append(dir)
        return dir_list
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    finally:
        return None

def Read(FileObj:object)->str:
   return FileObj.read()

def Cat(filename:str)->None:
    try:
        with open(filename,"rb") as fileobj:
            data=Read(FileObj=fileobj)
            logging.info(data)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    finally:
        return None

def cd(dir:str)->None:
    try:
        chdir(dir)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    finally:
        return None

def mkdir(dirname:str,dest:str|None=None)->None:
    try:
        if dest is None:
            os.mkdir(dirname)
            logging.info(f" created a new directory: {dirname}")
        else:
            cd(dirname)
            os.mkdir(dirname)
            logging.info(f" created a new directory in {dest}: {dirname}")
    except os.error as oserror:
        logging.error(f' {oserror}')
    finally:
        return None

def get_env_var(env_path:str,env_var:str)->str|None:
    """:env_path: str -> path to .env file (relatvie/absolute)
    :env_var: str -> variable to be searched
    """
    try:
        dotenv.load_dotenv(env_path)
        return os.getenv(env_var)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    finally:
        return None

def add_env_var(env_path:str,**env_var:dict[str,str])->None:
    """:env_path: str -> path to .env file (relatvie/absolute)
    :**env_var: dict[str,str] -> a pair of var:str and value:str
    """
    try:
        dotenv.load_dotenv(env_path)

        for key in env_var:
            dotenv.set_key(env_path,key_to_set=key,value_to_set=env_var[key])
    except FileExistsError:
        cd(env_path)
        logging.error(" File Does Not Exists!\n[#]Creating .env file in the specified path[#]")
        with open(".env","x") as f:
            pass
    except Exception as error:
        logging.error(f' {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}')
    else:
        logging.info(" Entered all the keys:values in .env file!")
    finally:
        return None

def remove_env_var(env_path:str,env_var:str)->None:
    """:env_path: str -> path to .env file (relatvie/absolute)
    :env_var: str -> variable to be removed from .env 
    """
    try:
        dotenv.load_dotenv(env_path)
        dotenv.unset_key(env_path,env_var)
    except FileExistsError:
        cd(env_path)
        logging.error(" File Does Not Exists!\n[#]Creating .env file in the specified path[#]")
        with open(".env","x") as f:
            pass
    except Exception as error:
        logging.error(f' {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}')
    else:
        logging.info(f" '{env_var}' has been removed from .env file!")
    finally:
        return None
    
def view_env_var(env_path:str,limit:int=15)->None:
    """:env_path: str -> path to .env file (relatvie/absolute)
    :limit: int -> limit to the number of varibles to view (default 15)
    """
    try:
        dotenv.load_dotenv(env_path)
        env=dotenv.dotenv_values()

        count=1
        for key in env:
            if count<=limit:
                print(f"{count:<3} {key}:{env[key]}")
            count+=1
        print("~~~~~~~~~~~~~~~~~~~~end of line~~~~~~~~~~~~~~~~~~~~")
        
    except FileExistsError:
        cd(env_path)
        logging.error(" File Does Not Exists!\n[#]Creating .env file in the specified path[#]")
        with open(".env","x") as f:
            pass
    except Exception as error:
        logging.error(f' {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}')
    finally:
        return None

def env_exists(env_path:str)->bool:
    """:env_path: str -> path to .env file (relatvie/absolute)"""
    try:
        dir_list=ls(dir=env_path)
        for dir in dir_list:
            if dir.endswith(".env") or ".env" in dir:
                return True
            else:
                return False
    except FileExistsError:
        return False
    except FileNotFoundError:
        return False

def copy_env(env_path:str,copy_env_path:str)->None:
    """:env_path: str -> path to .env file (relatvie/absolute)
    :copy_env_path: str -> path to .env files for it to be copy (absolute)
    """
    try:
        with open(env_path,"r") as env1:
            with open(copy_env_path,"a") as env2:
                for line in env1.readlines():
                    env2.write(line)
    except Exception as error:
        logging.error(f' {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}')
    finally:
        return None

def transfer(path:str,dest_path:str)->None:
    '''transfer
    ~~~~~~~~~~~~~~   
    :path: str -> Current path of file
    :dest_path: str -> destination path for the file to be transered
    '''
    try:
        move(path,dest_path)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    else:
        logging.info(f" Moved from {path} ---> {dest_path}")
    finally:
        return None

def delete_file(path:str)->bool:
    """:path: str -> path to file of any .extension to be deleted (absolute)"""
    try:
        os.remove(path)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
        return False
    else:
        return True

def get_current_dir()->str:
    """Returns the current directory that python is in. (str)
    ~~~~"""
    return os.getcwd()

def clear_env(env_path:str)->None:
    """:env_path: str -> path to .env file (relatvie/absolute)"""
    try:
        with open(env_path,"w") as fileobj:
            fileobj.write("")
    except Exception as error:
        logging.error(f' {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}')
    else:
        logging.info(f"Cleared .env file in '{env_path}'")

def create_env(dir:str|None=None)->None:
    """:dir: str -> directory to create .env file (relatvie/absolute)"""
    current_dir=get_current_dir()
    try:
        if dir is None:
            with open(".env","x") as f:
                logging.info(f" Created a .env file in '{get_current_dir()}' <---- current dir as dir was not specified!")
        else:
            cd(dir=dir)
            with open(".env","x") as f:
                logging.info(f" Created a .env file in '{get_current_dir()}'")
            cd(current_dir)
    except Exception as error:
        logging.error(f" {CustomColor(255,0,0).rgb()}{error}{TextFormatter.RESET}")
    finally:
        return None
