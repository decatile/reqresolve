class PackageNotFoundException(Exception):
    def __init__(self, package: str):
        super().__init__(f'Unable to find package {package}')

class NoSuitableVersionException(Exception):
    def __init__(self, package: str):
        super().__init__(f'Unable to find suitable version of package {package}')
