=================================
Changelog for django-agnocomplete
=================================

master (unreleased)
===================

- Now ready for Python 3.5. (#19) - Note: Only available for Django 1.8 and above.


0.4.0 (2016-02-04)
==================

- Added the multiple selection feature (#33).


0.3.2 (2016-01-27)
==================

- added a new method in ``AgnocompleteModel``, named ``build_filtered_queryset``, to allow overriding (#47).


0.3.1 (2015-12-04)
==================

- Fix IE8/9 bug for AJAX response headers (#45)


0.3.0 (2015-11-06)
==================

- Stronger validation of context-based agnocomplete fields (#39).
- Expose a ``final_queryset`` (aliasing the ``_final_queryset`` property) *and* a ``final_raw_queryset`` property that recieves the actual *unpaginated* queryset on which the search is based (#40).


0.2.3 (2015-11-05)
==================

- Expose a ``_final_queryset`` property that receives the actual queryset executed right before serialization (#40).


0.2.2 (2015-10-12)
==================

- Improve performances by slicing the resultset before rendering (#36).
- Added an `item(current_item)` method to override display label on choices (#37).


0.2.1 (2015-09-30)
==================

- Add a new method to have the possibilty to override easily the display label (#34).
- ``make docs`` is a PHONY makefile target.

0.2.0 (2015-09-17)
==================

Feature(s)
----------

- a more pertinent data attribute to target agnocomplete-ready fields (#22).
- New Demo: using ``jquery-autocomplete`` (#10, thx @GreatWizard).
- New Demo: using twitter's ``typeahead`` (#23, thx @GreatWizard).
- New Demo: using ``select2`` (#24, thx @GreatWizard).
- Fixed bad Django 1.6 loading (#29).
- Added the Admin site demo, along with documentation (#27).

Minor changes
-------------

- Post-v0.1 cleanups (#18),
- Introduced interface contract using the ``@abstractmethod`` decorator. This doesn't change anything for the user, but it makes sure that classes that don't implement the right methods can't even be instanciated (#25, thx @boblefrag).
- Modularized the demo-specific Javascripts in ``static/js/demo/`` (#28).
- Documentation about hacking and fiddling with the demo site (#30)

v0.1.0 (2015-09-11)
===================

First official release, yay!

Features
--------

* Define your Autocomplete classes to offer a list of choices, based on static data or Django models,
* Customize the data source to adjust to your business logic: filter based on static flags (``is_active=True``) or on the user-context (filter users that share the same customer_id that the current user),
* Create forms with Agnocomplete-ready fields ; standard usage doesn't need anymore cutomization or tweaking,
* Integrate these barebone forms with **the JS front-end you want**. We're simply providing a simple automatically generated API,
* Customize almost everything: query size, page size, target URL, target views,...
* Read the full documentation on standard usage and customization howto's,
* Browse the demo website with simple backend/frontend samples,
* Use this lib with python 2.7, 3.3, 3.4 and Django 1.6, 1.7, 1.8 (thank you tox!).
* Use, hack, redistribute, contribute, because it's MIT-Licensed.
