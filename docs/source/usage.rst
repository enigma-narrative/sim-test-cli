Usage
=====

mct init
--------

Create an ``.mctrc`` file in the current directory.

.. code-block:: bash

   mct init --username jyurkiw [--template_site_path https://github.com] [template ...]

The first template name given (if any) is automatically set as the
``default_template``.

mct set default
----------------

Set the default template used by ``mct new`` when ``--template`` is
omitted. The given name must already be in the ``templates`` list — an
unknown name is rejected and ``.mctrc`` is left unchanged.

.. code-block:: bash

   mct set default my-template

mct ls
------

List all templates recorded in the active ``.mctrc``.

.. code-block:: bash

   mct ls

mct add
-------

Show the templates you're about to add in a table, then ask for
confirmation (``[y/N]``, default no) before appending them to ``.mctrc``.

.. code-block:: bash

   mct add my-template another-template

mct rm
------

Show every template name involved (the union of what's already recorded and
what you passed) in a table with a status column:

* ``DELETE`` — passed on the command line and currently recorded
* ``KEEP`` — recorded but not passed
* ``NO EXIST`` — passed but not currently recorded

After confirmation (``[y/N]``, default no), the ``DELETE`` entries are
removed from ``.mctrc``.

.. code-block:: bash

   mct rm my-template

mct new
-------

Clone a template repository under a new name and repoint its ``origin``
remote at the new project's (not-necessarily-yet-existing) repository URL.

.. code-block:: bash

   mct new --template my-template my-new-project

If ``--template`` is omitted, the ``default_template`` from ``.mctrc`` is
used instead. If neither is available, ``mct new`` exits with an error.

Before cloning, ``mct new``:

1. Confirms the git hosting site is reachable.
2. Confirms the template repository exists (via ``git ls-remote``).
3. Confirms the destination directory name isn't already in use.

After cloning and repointing the remote, it checks whether the new
repository already exists on the hosting site and tells you either that you
can push now, or that you need to create the remote repository first.

``--template_site_path`` and ``--username`` can be passed to override the
values from the discovered ``.mctrc`` for that single invocation.
