#!venv/bin/python
import subprocess
from typing import List
from app import dbsession
from db.model import Package, Tag
import numpy as np
import argparse


class PackageTableUpdater():
    def read_package_list(self) -> np.ndarray:
        output = subprocess.check_output(['pacman', '-Sl'], encoding='utf8')
        lines = output.splitlines()
        return np.asarray(lines)

    def read_aur_package_list(self) -> np.ndarray:
        output = subprocess.check_output(['yay', '-Sl', 'aur'], encoding='utf8')
        lines = output.splitlines()
        return np.asarray(lines)

    def get_package_info(self, line: str) -> tuple:
        line = str(line).split(" ")
        return (line[1], line[0])
    
    def upload_new_packages(self, packages: np.ndarray) -> None:
        for i in range(0, packages.size):
            [name, repo] = self.get_package_info(packages[i])
            item: Package = dbsession.query(Package).filter(Package.name_id == name).first()
            if item is None:
                dbsession.add(Package(name_id=name, repository=repo))
            else:
                if item.repository != repo:
                    item.repository = repo
        dbsession.commit()

    def update_package_list(self) -> None:
        self.upload_new_packages(self.read_package_list())
        self.upload_new_packages(self.read_aur_package_list())
        #delete deleted packages?
    
    def delete_row(self, id) -> bool:
        tag = dbsession.query(Tag).filter(Tag.name_id == id).first()
        if (tag == None): return False
        dbsession.delete(tag)
        dbsession.commit()

    def add_tag(self, id, name) -> bool:
        dbsession.add(Tag(name_id=id, nice_name=name))
        dbsession.commit()


if __name__ == '__main__':
    updater = PackageTableUpdater()
    parser = argparse.ArgumentParser(prog='dbUtil', description='Database Utility')
    parser.add_argument('--dt', dest='tag_id', help='delete a Tag based on id')
    parser.add_argument('--at', dest='new_tag_id', help='add a Tag')

    args = vars(parser.parse_args())
    if (args.get('tag_id', None) is not None):
        updater.delete_row(args.get('tag_id'))
    if (args.get('new_tag_id', None) is not None):
        updater.delete_row(args.get('tag_id'))
        

    updater.update_package_list()
