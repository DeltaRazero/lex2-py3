
# lex2-py3

<img align="right" width=40em src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg">

<!-- BADGES -->
<div align="left">
    <!--
        Python3 version
    --->
    <img src="https://img.shields.io/badge/python-3.6+-informational.svg?labelColor=363d45&logo=python&logoColor=white"
    alt="Python 3.6+"/>
    <!--
        Library tag version
    --->
    <a href="https://github.com/deltarazero/lex2-py3/tags">
        <img src="https://img.shields.io/github/v/tag/deltarazero/lex2-py3?labelColor=363d45&logo=github&logoColor=white"
        alt="Latest release tag version"/></a>
    <!--
        Issues open
    --->
    <a href="https://github.com/deltarazero/lex2-py3/issues">
        <img src="https://img.shields.io/github/issues/deltarazero/lex2-py3?labelColor=363d45&logo=github&logoColor=white"
        alt="GitHub issues open"/></a>
    <!--
        License
    --->
    <a href="https://choosealicense.com/licenses/zlib/">
        <img src="https://img.shields.io/github/license/DeltaRazero/lex2-py3?labelColor=363d45&color=informational"
        alt="zlib license"/></a>
</div>

<!-- BUTTON LINKS -->
<div align="left">
    <!--
        Documentation
    --->
    <a href="https://deltarazero.github.io/lex2-py3/">
        <img src="https://img.shields.io/badge/-Documentation_»-363d45"
        height="24"
        alt="[Documentation]"/></a>
</div>

<div align="justify"><br/>

lex2 is a library intended for [lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis) (also called [tokenization](https://en.wikipedia.org/wiki/Lexical_analysis)). String analysis is performed using [regular expressions (regex)](https://en.wikipedia.org/wiki/Regular_expression) in user-defined rules. Some additional functions, such as dynamic ruleset stack, provide flexibility to some degree at runtime.

The library is written in platform independent pure Python3, and is portable (no usage of language-specific features) making it straightforward to port to other programming languages. Furthermore, the library is designed to enable the end-user to easily integrate any external regex engine of their choice through a simple to use unified interface.


## Getting Started

As per usual, you can install the library from the Python Package Index (PyPI) through ``pip``:
```console
pip install lex2
```

You can also choose to manually include the library in your project by cloning or downloading a snapshot of the repository from GitHub and copying the ``lex2`` folder to your project's includes/libraries folder.

Usage of the library is relatively simple, demonstrated by the short example below. For more in-depth examples and using a different regex engines of your choice, see the documentation.

```python
import lex2

# Define ruleset and prepare the lexer object instance
ruleset: lex2.RulesetType = [
    #        Identifier     Regex pattern
    lex2.Rule("WORD",        r"[a-zA-Z]+"),
    lex2.Rule("NUMBER",      r"[0-9]+"),
    lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
]
lexer: lex2.ILexer = lex2.make_lexer()(ruleset)

# Load input data by opening a file
lexer.open(r"C:/path/to/file.txt")
# Or by directly passing a string
lexer.load("The quick, brown fox jumps over 2 lazy dogs. \nMr. Jock, TV quiz PhD, bags few lynx.")

# Main tokenization loop
token: lex2.Token
while(1):

    # Find the next token in the textstream
    try: token = lexer.get_next_token()
    except lex2.excs.EOD:
        break

    info = [
         "ln: {}".format(token.pos.ln +1),
        "col: {}".format(token.pos.col+1),
        token.id,
        token.data,
    ]
    print("{: <12} {: <15} {: <20} {: <20}".format(*info))

lexer.close()
```

```console
>>> ln: 1        col: 1          WORD                 The
>>> ln: 1        col: 5          WORD                 quick
>>> ln: 1        col: 10         PUNCTUATION          ,
>>> ln: 1        col: 12         WORD                 brown
>>> ln: 1        col: 18         WORD                 fox
>>> ln: 1        col: 22         WORD                 jumps
>>> ln: 1        col: 28         WORD                 over
>>> ln: 1        col: 33         NUMBER               2
>>> ln: 1        col: 35         WORD                 lazy
>>> ln: 1        col: 40         WORD                 dogs
>>> ln: 1        col: 44         PUNCTUATION          .
>>> ln: 2        col: 1          WORD                 Mr
>>> ln: 2        col: 3          PUNCTUATION          .
>>> ln: 2        col: 5          WORD                 Jock
>>> ln: 2        col: 9          PUNCTUATION          ,
>>> ln: 2        col: 11         WORD                 TV
>>> ln: 2        col: 14         WORD                 quiz
>>> ln: 2        col: 19         WORD                 PhD
>>> ln: 2        col: 22         PUNCTUATION          ,
>>> ln: 2        col: 24         WORD                 bags
>>> ln: 2        col: 29         WORD                 few
>>> ln: 2        col: 33         WORD                 lynx
>>> ln: 2        col: 37         PUNCTUATION          .
```


## Development Dependencies

For development you will need the following dependencies:
* Python:
    * Version 3.8+
    * Packages can be installed via `requirements.txt`, using the following command:
      ```console
      pip install -r requirements.txt
      ```
* Documentation (for diagrams via PlantUML)
    * Java
    * Graphiz


## Contributing

The repository is hosted at [deltarazero/lex2-py3](https://github.com/deltarazero/lex2-py3) on GitHub. Contribution is always welcome; you can contribute by satisfying one of the following points of action:

* __Submitting a pull request:__ to contribute your own changes to the repository. See ["Proposing changes to your work with pull requests"](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests) for more information on pull requests using GitHub. Furthermore, please follow the guidelines below:

    - File an issue to notify the maintainers about what you're working on.
    - Fork the repo, develop and test your code changes, add docs/unit tests (if applicable).
    - Make sure that your commit messages clearly describe the changes.
    - Send a pull request, using the available template.

    For changes that address core functionality or would require breaking changes (i.e. for a major release), it's best to open an issue to discuss your proposal beforehand.

    _Maintaining your own fork of the repository is discouraged. Instead, please submit pull requests and delete your fork afterwards (if applicable). This will make it less confusing for end-users to know which repository is the most up-to-date._

* __Submitting an issue:__ to report a problem with the library, request a new feature, or to discuss potential changes before a pull request is created. Ensure the issue was not already reported. Furthermore, please use one of the available issue templates if possible.


## License

© 2020-2022 DeltaRazero.
All rights reserved.

All included scripts, modules, etc. are licensed under the terms of the [zlib license](https://github.com/deltarazero/lex2-py3/LICENSE), unless stated otherwise in the respective files.

</div>
