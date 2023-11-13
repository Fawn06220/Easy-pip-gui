from distutils.core import setup
setup(
  name = 'easy-pip-gui',         # How you named your package folder (MyLib)
  packages = ['easy-pip-gui'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An easy pip GUI',   # Give a short description about your library
  author = 'François Garbez',                   # Type in your name
  author_email = 'fawn06220@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Fawn06220/Easy-pip-gui',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Fawn06220/Easy-pip-gui/archive/v_1.0.tar.gz',    # I explain this later on
  keywords = ['python', 'pip', 'gui'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'wxpython',
          'pip-api',
          'pip-review',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.12',
  ],
)
