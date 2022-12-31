
import os
import paramiko
from stat import S_ISREG


directory = os.path.dirname(os.path.realpath(__file__))


paramiko.Transport._preferred_kex = ('diffie-hellman-group-exchange-sha256',
                                     'diffie-hellman-group14-sha256',
                                     'diffie-hellman-group-exchange-sha1',
                                     'diffie-hellman-group14-sha1',
                                     'diffie-hellman-group1-sha1')


known_hosts_filepath = os.path.join(directory, 'known_hosts')
if not os.path.exists(known_hosts_filepath):
    with open(known_hosts_filepath, 'w') as f:
        pass


class SFTP(paramiko.SSHClient):
    def __init__(self
                 , ftp_host=os.getenv('ftp_host')
                 , ftp_uid=os.getenv('ftp_uid')
                 , ftp_pwd=os.getenv('ftp_pwd')
                 , port=22
                 , trust_connection = False
                 ):
        self.ftp_host = ftp_host
        self.ftp_uid = ftp_uid
        self.ftp_pwd = ftp_pwd
        self.port = port
        super().__init__()
        self.load_host_keys(known_hosts_filepath)
        if trust_connection == True:
            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            self.set_missing_host_key_policy(paramiko.RejectPolicy())

    def get(self, source_file, destination_file):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port, timeout=60*90)
        self.open_sftp().get(source_file, destination_file)
        self.close()

    def put(self, source_file, destination_file):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port)
        self.open_sftp().put(source_file, destination_file)
        self.close()

    def listdir(self, directory=''):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port)
        dir_list = self.open_sftp().listdir(directory)
        self.close()
        return dir_list

    def isfile(self, file_path):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port)
        try:
            file_path_exists = S_ISREG(self.open_sftp().stat(file_path).st_mode)
        except IOError:     # no such file
            file_path_exists = False
        self.close()
        return file_path_exists

    def remove(self, source_file):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port)
        self.open_sftp().remove(source_file)
        self.close()

    def mkdir(self, directory):
        self.connect(hostname=self.ftp_host, username=self.ftp_uid, password=self.ftp_pwd, port=self.port)
        try:
            self.open_sftp().chdir(directory)
        except:
            self.open_sftp().mkdir(directory)
        self.close()