#!/usr/bin/python
import nose
from testify import Testify

if __name__ == '__main__':
	nose.main(addplugins = [Testify()])
