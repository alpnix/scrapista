.. _settingup:

Setting Up Scrapista
====================

Scrapista is viable in **Windows**, **Mac** and **Linux** as long as there is python installed in your device. In addition to scrapista, you also need 'Beautiful Soup' and 'requests' which are automatically installed with scrapista because scrapista depends on these packages. 

Installing Scrapista 
---------------------
There are barely any requirements for getting started with scrapista!

- First of all, you need to make sure you have python installed on your computer. You can visit `Python's official site <https://www.python.org/downloads/>`_ and download Python from right there. 

- You need to have 2.7 or a higher version of Python installed in your computer. You can check this by ``$ python --version`` command in the terminal you use.

After that you can directly install scrapista on your Python environment by ``$ python -m install scrapista`` or ``$ pip install scrapista`` command. 

If you are on a **Linux** device,

You might want to try ``$ python3 -m install scrapista`` or ``$ pip3 install scrapista`` commands instead of the prior ones. 

.. _installationproblems:

Problems After Installation
------------------------------

Import scrapista on the program you are using as seen below and run it to if any error occurs.::

    import scrapista

    dir(scrapista)

Unless an error occurs when you run the program, you are ready to go with either :ref:`quick start<gettingstarted>` or importing classes.

If you encounter a ``ModuleNotFound`` error at this stage, then you have to make sure you have scrapista on the same environment as the one you are trying to run this program with. 

After you make sure you have scrapista installed on your environment you might also want to check if you have 'requests' and 'Beautiful Soup' as scrapista is dependant on them both. 
