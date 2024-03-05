#from distutils.core import setup 
#from Cython.Distutils import build_ext 
#from distutils.extension import Extension 
from setuptools import setup, Extension

                         
setup(
      name='DP_GP_cluster',
      version='0.1',
      description='Clustering gene expression time course data by an infinite Gaussian process mixture model.',
      url='https://github.com/ReddyLab/DP_GP_cluster',
      author='Ian McDowell, Dinesh Manandhar, Barbara Engelhardt',
      author_email='ian.mcdowell@duke.edu',
      keywords = ['clustering','Dirichlet Process', 'Gaussian Process', \
                  'Bayesian', 'gene expression', 'time series'],
      license='BSD License',
      packages=['DP_GP'],
      setup_requires=['numpy', 'Cython'],
      install_requires=["matplotlib", "numpy", "pandas", "scipy", "scikit-learn", "GPy"],
      package_dir={'DP_GP':'DP_GP'},
      scripts=['bin/DP_GP_cluster.py'],
      long_description=open('README.md', 'rt').read()
     )
