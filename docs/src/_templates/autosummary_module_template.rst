{{ fullname | escape | underline }}
.. Page title

.. This will only display the module's docstring
.. automodule:: {{ fullname }}
    :no-members:


.. Table of (sub)modules
{% block modules %}
{% if modules %}
.. rubric:: Modules

.. autosummary::
   :toctree:
   :template: autosummary_module_template.rst
   :recursive:
{% for item in modules %}
    {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


.. Table of attributes
{% block attributes %}
{% if attributes %}
.. rubric:: Attributes

.. autosummary::
{% for item in attributes %}
    {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


.. Table of classes
{% block classes %}
{% if classes %}
.. rubric:: {{ _('Classes') }}

.. autosummary::
{% for item in classes %}
    {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


.. Table of functions
{% block functions %}
{% if functions %}
.. rubric:: {{ _('Functions') }}

.. autosummary::
{% for item in functions %}
    {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


.. Table of exceptions
{% block exceptions %}
{% if exceptions %}
.. rubric:: {{ _('Exceptions') }}

.. autosummary::
{% for item in exceptions %}
    {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


.. Document all components within the current (sub)module
.. Undocumented members are not included (or you need to add :undoc-members:)
.. automodule:: {{ fullname }}
    :no-value:
    :members:
    :imported-members:
    :no-undoc-members:
