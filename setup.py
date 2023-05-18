import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Stabl',
    version='0.0.1',
    author='Gregoire Bellan',
    author_email='gbellan@surge.care',
    description='Stabl package',
    packages=['stabl', 
              'STABLapp_utils',
              'STABLapp_utils.subwindows',
              'STABLapp_utils.ScriptComponents',
              'STABLapp_utils.Subframes',
              'STABLapp_utils.SubframeComponents.ConfirmationWindow',
              'STABLapp_utils.SubframeComponents.Files',
              'STABLapp_utils.SubframeComponents.Pipeline',
              'STABLapp_utils.SubframeComponents.Sbatch',
              'STABLapp_utils.SubframeComponents.Stabl'],
    install_requires=[
        'scikit-learn>=1.1.2',
        'knockpy>=1.2',
        'pandas>=1.4.2',
        'numpy>=1.23.1',
        'joblib>=1.1.0',
        'tqdm>=4.64.0',
        'seaborn>=0.12.0',
        'matplotlib>=3.5.2',
        'customtkinter'
    ]
)