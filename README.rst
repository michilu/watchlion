Watch Lion
==========
A simple shell utility to monitor file system events on Mac OS X 10.7+ (Lion or newer).


Shell Utilities
---------------
Watch Lion comes with a utility script called ``watchlion``.
Please type ``watchlion --help`` at the shell prompt to
know more about this tool.

``watchlion`` can read ``.watchlion.yml`` files and execute command within them in
response to file system events. The ``.watchlion.yml`` file will be monitored and
loading when it has been updated.

An example ``.watchlion.yml`` file::

  build:
    coffee: make js
    haml:   make html
    py:     make test
    sass:   make css
  loglevel: info

An example ``Makefile`` file::

  .SUFFIXES: .coffee .js
  .coffee.js:
  	coffee -b -c $<
  .SUFFIXES: .js .min.js
  .js.min.js:
  	uglifyjs -nc -o $@ $<
  COFFEE = $(wildcard *.coffee)
  JS = $(COFFEE:.coffee=.js)
  MINJS = $(JS:.js=.min.js)

  .SUFFIXES: .haml .html
  .haml.html:
  	haml -f html5 -t ugly $< $@
  HAML = $(wildcard *.haml)
  HTML = $(HAML:.haml=.html)

  .SUFFIXES: .sass .css
  .sass.css:
  	compass compile $< -c config.rb
  .SUFFIXES: .sass .min.css
  .sass.min.css:
  	compass compile --environment production $< -c config.rb
  	mv $*.css $@
  SASS = $(wildcard *.sass)
  CSS = $(SASS:.sass=.css)
  MINCSS = $(SASS:.sass=.min.css)

  css: $(MINCSS) $(CSS)
  html: $(HTML)
  js: $(JS) $(MINJS)
  test:
  	py.test

Then run ``watchlion`` command::

  $ watchlion
  INFO:root:load_config: loading .watchlion.yml
  ...

Will start building js files when you update a coffee file::

  ...
  INFO:root:make js
  coffee -b -c main.coffee
  uglifyjs -nc -o main.min.js main.js
  ...

You can use control-C to stop ``watchlion`` .


Installation
------------
Installing from PyPI using ``pip``::

    pip install watchlion

Installing from PyPI using ``easy_install``::

    easy_install watchlion

Installing from source::

    python setup.py install


Installation Caveats
~~~~~~~~~~~~~~~~~~~~
The ``watchlion`` script depends on PyYAML_ which links with LibYAML_,
which brings a performance boost to the PyYAML parser. However, installing
LibYAML_ is optional but recommended. On Mac OS X, you can use homebrew_
to install LibYAML::

    brew install libyaml

Supported Platforms
-------------------
* Mac OS X 10.7+ (require FSEvents_)


Dependencies
------------
1. Python 2.6 or above.
2. XCode_
3. PyYAML_


Licensing
---------
Watch Lion is licensed under the terms of the MIT_.

Copyright 2012 ENDOH takanao.

Project `source code`_ is available at Github. Please report bugs and file
enhancement requests at the `issue tracker`_.


.. links:
.. _source code: http://github.com/MiCHiLU/watchlion
.. _issue tracker: http://github.com/MiCHiLU/watchlion/issues
.. _MIT: http://opensource.org/licenses/MIT

.. _homebrew: http://mxcl.github.com/homebrew/
.. _PyYAML: http://www.pyyaml.org/
.. _FSEvents: http://developer.apple.com/documentation/Darwin/Conceptual/FSEvents_ProgGuide/
.. _XCode: http://developer.apple.com/technologies/tools/xcode.html
.. _LibYAML: http://pyyaml.org/wiki/LibYAML
