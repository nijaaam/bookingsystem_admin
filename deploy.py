#!/usr/bin/env python
from deployer.client import start
from deployer.node import Node, required_property
from deployer.utils import esc1
from deployer.host import SSHHost
from deployer.exceptions import ActionException

home = '/home/main/'
ip = 'bksysadmintestin3645.cloudapp.net'
project_name = "bookingsystem_admin/"
virtualenv = "BKSYSDEPLOY/"
project_dir = home + virtualenv + project_name
repo = 'https://github.com/nijaaam/bookingsystem_admin.git'
keyLocation = '/home/nijam/Desktop/keys/bookingsystem'
cronLog = '/var/log/cronjobs/'

class VirtualEnv(Node):
    location = required_property()
    requirements_files = []
    packages = []

    @property
    def activate_cmd(self):
        return  '. %sbin/activate' % self.location

    def install_requirements(self):
        with self.hosts.prefix(self.activate_cmd):
            for f in self.requirements_files:
                self.hosts.sudo("pip install -r '%s' " % esc1(f))

    def install_package(self, name):
        with self.hosts.prefix(self.activate_cmd):
            self.hosts.run("pip install '%s'" % name)

    def setup_env(self):
        for p in self.packages:
            self.install_package(p)
        self.install_requirements()

    def run_management_command(self, command):
        with self.hosts.prefix(self.activate_cmd):
            with self.hosts.cd(project_dir):
                self.hosts.run('./manage.py %s' % command)

    def run_uwsgi(self):
        with self.hosts.prefix(self.activate_cmd):
            with self.hosts.cd(project_dir):
                self.hosts.run('uwsgi start_app.ini')

    def collectstatic(self):
        self.run_management_command('collectstatic --clear --noinput --settings=bookingsystem_admin.production')

    def update_database(self):
        self.run_management_command('migrate --noinput --settings=bookingsystem_admin.production')

    def clean(self):
        with self.hosts.cd(project_dir):
            self.hosts.run('find . -name \'*.py?\' -exec rm -rf {} \;')

class Git(Node):
    project_directory = required_property()
    repository = required_property()

    def install(self):
        self.hosts.sudo('apt-get install git')

    def clone(self):
        with self.hosts.cd(self.project_directory, expand=True):
            self.hosts.run("git clone '%s'" % esc1(self.repository))

    def pull(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                try:
                    self.hosts.run("git pull")
                except ActionException:
                    self.stash()
                    self.pull()
    def stash(self):
        with self.hosts.cd(self.project_directory, expand=True):
            with self.hosts.cd(project_dir):
                self.hosts.run("git stash")

    def checkout(self, commit):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.run("git checkout '%s'" % esc1(commit))

    def tag(self):
        with self.hosts.cd(project_dir, expand=True):
            self.hosts.run("git tag LIVE")
            self.hosts.run('export TAG="date +DEPLOYED-%F/%H%M"')
            self.hosts.run("git tag $TAG")
            self.hosts.run("git push origin LIVE $TAG")

class DjangoDeployment(Node):
    class virtual_env(VirtualEnv):
        location = home + virtualenv
        packages = []
        requirements_files = [project_dir + 'requirements.txt' ]

    class git(Git):
        project_directory = home + virtualenv
        repository = repo

    def setup(self):
        #self.git.checkout('release')
        self.virtual_env.clean()
        self.git.pull()
        self.virtual_env.setup_env()
        self.virtual_env.update_database()
        self.virtual_env.collectstatic()
        self.virtual_env.run_uwsgi()

    def checkIfCJexists(self):
        self.hosts.run('crontab -l')

    def addCJ(self):
        backup = '0 0 * * * main ' + project_dir + ' manage.py dbbackup > ' + cronLog
        backup = '{ crontab -l -u main; echo "'+ backup +'"; } | crontab -u main -'

        checkIfRunning = '@hourly ' + project_dir + ' manage.py checkIfRunning > ' + cronLog
        checkIfRunning = '{ crontab -l -u main; echo "'+ checkIfRunning +'"; } | crontab -u main -'

        runOnBoot = '@reboot ' + project_dir + 'runOnBoot.sh'
        
        runOnBoot = '{ crontab -l -u main; echo "'+ runOnBoot +'"; } | crontab -u main -'
        
        self.hosts.run(backup)
        self.hosts.run(checkIfRunning)
        self.hosts.run(runOnBoot)
    
    def fullSetup(self):
        self.hosts.sudo('apt-get update && apt-get install mysql-client-5.7 build-essential libssl-dev libffi-dev virtualenv uwsgi nginx libmysqlclient-dev python-pip')
        self.hosts.sudo('virtualenv ' + virtualenv)
        try:
            self.git.clone()
        except ActionException:
            pass
        self.virtual_env.setup_env()
        self.runSpecialCmd('rm /etc/nginx/sites-enabled/default')
        self.hosts.sudo('ln -f -s ' + project_dir + 'config/bksys.conf /etc/nginx/sites-enabled/')
        self.hosts.sudo('/etc/init.d/nginx restart')
        try:
            self.checkIfCJexists()
        except ActionException:
            self.addCJ()
        self.runSpecialCmd('mkdir /etc/uwsgi')
        self.runSpecialCmd('mkdir /etc/uwsgi/vassals')
        self.hosts.sudo('ln -f -s ' + project_dir + 'start_app.ini /etc/uwsgi/vassals/')
        self.hosts.run('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')

    def runSpecialCmd(self,cmd):
        try:
            self.hosts.sudo(cmd)
        except:
            pass

class remote_host(SSHHost):
    address = ip 
    username = 'main'       
    key_filename = keyLocation    

class DjangoDeploymentOnHost(DjangoDeployment):
    class Hosts:
        host = remote_host

if __name__ == '__main__':
    start(DjangoDeploymentOnHost)