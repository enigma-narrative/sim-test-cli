Configuration
=============

``mct`` reads its settings from an ``.mctrc`` TOML file. When you run any
command other than ``mct init``, ``mct`` searches the current directory and
then its parents, up to the drive root, for an ``.mctrc`` file. The first one
found (closest to the current directory) is the one used.

Schema
------

.. code-block:: toml

   template_site_path = "https://github.com"
   username = "jyurkiw"
   templates = ["my-template", "another-template"]
   default_template = "my-template"

``template_site_path``
   The base URL of the git hosting site (GitHub, Gitea, and — untested but
   likely compatible — GitLab).

``username``
   Your username on that hosting site.

``templates``
   The list of template repository names you maintain.

``default_template``
   The template used by ``mct new`` when ``--template`` is omitted. Set
   automatically to the first template passed to ``mct init``, and
   updatable afterward with ``mct set default <template_name>``. Not
   present if no templates were given at init time and none has been set
   since.

Repository addresses are assembled as::

   {template_site_path}/{username}/{repo_name}
