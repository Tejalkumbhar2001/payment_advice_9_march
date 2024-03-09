from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in payment_advice/__init__.py
from payment_advice import __version__ as version

setup(
	name="payment_advice",
	version=version,
	description="advice for payment",
	author="quantbit technology",
	author_email="contact@erpdata.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
