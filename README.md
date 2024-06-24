chatgpt-client
==============
A ChatGPT client in wxPython.

Usage
-----
```
export OPENAI_API_KEY=sk-foobarbaz
export OPENAI_API_ORG=org-foobarbaz
python3 client.py
```

### Subcommands
* `/sw msgIdx branchIdx` - switches a message to a different sibling branch
* `/nb msgIdx content content content ...` - creates a new sibling of a message
  * content is required to create a sibling of a user message
  * content is ignored when creating a sibling of a ChatGPT message

Limitations
-----------
* fixed system message
* can't delete convos
* probably pretty brittle i dunno lol

License
-------
Apache-2.0 (see LICENSE.txt)

Other disclosures
-----------------
ChatGPT 3.5 was used in the authoring of this work in the following capacities:
* To draft GUI initialization code.
* To generate examples for tasks in wxPython.
* To refactor certain code.
* To generate and refine initial implementations for menial tasks (e.g. the
  command parser)