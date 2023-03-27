import os
import shutil
import subprocess
import tarfile
from datetime import datetime

from config import MONGODUMP_DEFAULT_OUTPUT_DIR

from . import mongodump_logger

NONE_OR_STRING = [None, str]
NONE_OR_INT = [None, int]
TRUE_OR_FALSE = [True, False]

class MongoDump():
    def __init__(
        self,
        host: NONE_OR_STRING=None,
        port: NONE_OR_INT=None,
        username: NONE_OR_STRING=None,
        password: NONE_OR_STRING=None,
        db: NONE_OR_STRING=None,
        out: str=MONGODUMP_DEFAULT_OUTPUT_DIR,
        authenticationDatabase: NONE_OR_STRING=None,
        numParallelCollections: NONE_OR_INT=None
        ) -> None:
        self.db = db
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        if out.startswith('./'):
            self.out = os.path.abspath(out[2:])
        else:
            self.out = out
        self.authenticationDatabase = authenticationDatabase
        self.numParallelCollections = numParallelCollections

        if not out:
            llt = 'It is necessary to inform the output in ' \
                'the config.py(MONGODUMP_DEFAULT_OUTPUT_DIR) ' \
                    'file or directly in the variable.'
            mongodump_logger.error(llt)
            raise ValueError(llt)

    
    def dump(self):
        """
        Return:
            tuple(bool, str) => success, backup_path
        """

        mongodump_logger.info(
            'Starting mongodump on: ' \
                f'*{(self.db if self.db else "All")}* database'
            )

        self.__create_output_directory()

        cmd = self.__create_command_string().strip()
        mongodump_logger.info('Cmd dump: ' + cmd)

        try:
            with subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE) as proc:
                out = proc.stdout.read()
                mongodump_logger.info(out)
                print(out)

            mongodump_logger.info('Backup performed successfully.')
        except subprocess.CalledProcessError as cpe:
            llt = f'Backup error: {cpe}'
            mongodump_logger.error(llt)
            with open(self.out_with_date+'/dumperr.txt', 'a') as ffile:
                ffile.close()
            
            print('An error has occurred. Details in the log file at /logs')
            exit()
        
        with open(self.out_with_date+'/dumpsuccess.txt', 'a') as ffile:
            ffile.close()

        return (True, self.out_with_date)

    
    def compress_backup(
        self,
        backup_path,
        delete_original_files: TRUE_OR_FALSE=True
        ):
        """
        Backup compression reduces the backup size by more than 50% without affecting it.
        
        Return:
            tuple(bool, str) => success, compressed_backup_path
        """

        mongodump_logger.info(f'Starting compress_backup on: {backup_path}')

        targz_filename = 'backup.tar.gz'

        if not os.path.exists(backup_path + f'/{targz_filename}'):
        
            dirs = os.listdir(backup_path)
            if not dirs:
                llt = f"The path '{backup_path}' has no backup dirs to compress."
                mongodump_logger.error(llt)
                raise Exception(llt)

            try:
                with tarfile.open((backup_path + f'/{targz_filename}'), "w:gz") as tar:
                    for dir_ in dirs:
                        if os.path.isdir(backup_path + f'/{dir_}'):
                            tar.add(backup_path + f'/{dir_}')



                if delete_original_files is True:
                    for dir_ in dirs:
                        if os.path.isdir(backup_path + f'/{dir_}'):
                            shutil.rmtree(backup_path + f'/{dir_}')

            except Exception as err:
                llt = f'Error compress_backup: {err}'
                mongodump_logger.error(llt)
                raise err
        
        return (True, backup_path + f'/{targz_filename}')


    def __create_output_directory(self):
        
        self.out_with_date = self.out
        if self.out.endswith('/'):
            self.out_with_date += datetime.utcnow().strftime("%m-%d-%Y--%H-%M-%S")
        else:
            self.out_with_date += '/' + datetime.utcnow().strftime("%m-%d-%Y--%H-%M-%S")
        
        if not os.path.exists(self.out_with_date):
            path = os.path.abspath(self.out_with_date)
            os.makedirs(path)
            
            mongodump_logger.info(
                f'*{self.out_with_date}* Backup directory created.'
            )

        return True


    def __create_command_string(self):
        cmd = 'mongodump '
        accepted_parameters = [
            'db', 'host', 'port',
            'username', 'password',
            'out', 'authenticationDatabase',
            'numParallelCollections'
        ]
        
        for parameter in accepted_parameters:
            parameter_value = getattr(self, parameter)
            if parameter_value:
                if not parameter == 'out':
                    cmd += f'--{parameter} {parameter_value} '
                else:
                    cmd += f'--{parameter} {self.out_with_date} '

        return cmd



    
    # def test(self):
    #     return self.__create_output_directory()
