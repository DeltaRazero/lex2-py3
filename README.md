
<!-- HEADER -->
<div align="center">
    <!--
        Title
    --->
    <h1>
        <img src="https://github.com/DeltaRazero/liblex2-py3/blob/master/.rsrc/lex2_logo.svg"
        height="60"><br>
        liblex2-py3
    </h1>
    <!--
        One-line summary
    --->
    <p><b>
        Simple tokenizer using regex.
    </p></b>
</div>


<!-- BADGES -->
<div align="center">
    <!--
        License
    --->
    <a href="https://choosealicense.com/licenses/zlib/">
        <img src="https://img.shields.io/badge/license-zlib-informational.svg?labelColor=363d45"
        alt="zlib license"/></a>
    <!--
        Library tag version
    --->
    <a href="https://github.com/deltarazero/liblex2-py3/tags">
        <img src="https://img.shields.io/github/v/tag/deltarazero/liblex2-py3?labelColor=363d45&logo=github&logoColor=white"
        alt="Latest release tag version"/></a>
    <!--
        Issues open
    --->
    <a href="https://github.com/deltarazero/liblex2-py3/issues">
        <img src="https://img.shields.io/github/issues/deltarazero/liblex2-py3?labelColor=363d45&logo=github&logoColor=white"
        alt="GitHub issues open"/></a>
    <!--
        Python3 version
    --->
    <img src="https://img.shields.io/badge/python-3.6+-informational.svg?labelColor=363d45&logo=python&logoColor=white"
    alt="Python 3.6+"/>
</div>

<!-- BUTTON LINKS -->
<div align="center">
    <!--
        Documentation
    --->
    <!--
    <a href="https://deltarazero.github.io/liblex2-py3">
        <img src="https://img.shields.io/badge/-Documentation_»-informational"
        height="24"
        alt="[Documentation]"/></a>
    --->
    <!--
        Changelog
    --->
    <!--
    <a href="https://github.com/DeltaRazero/liblex2-py3/blob/master/CHANGELOG.md">
        <img src="https://img.shields.io/badge/-Changelog_»-informational"
        height="24"
        alt="[Changelog]"/></a>
    --->
</div>

<div align="center">
    <br/>
    <b>NOTE:</b> Documentation coming soon.
</div>



## About

"lex2" is a library to perform **lexical analysis** (often called **tokenization**). Rulesets are defined and scanned using **regular expressions (regex)**. Mechanisms such as the ruleset-stack and setting processing options provide flexibility to some degree at runtime.

The library is written as platform independent, pure Python3. Customization for adding a different regex engine implementation is very effortless whilst remaining to have a simple to use, unified interface for implementation-independent usage.



## Quickstart

Recommended is to install the library from the Python Package Index (PyPI) through Python's package manager ``pip``:
```console
pip install lex2
```
However, you can also choose to manually install the library by download a release on GitHub and copying the ``lex2`` folder to your project's includes/libraries directory.

Usage of lex2 is relatively simple, as demonstrated by the short example below. Nonetheless, it it still encouraged to read the documentation for more in-depth examples.

```python
import lex2

# Define ruleset and prepare the lexer object instance
ruleset: lex2.ruleset_t = [
    #        Identifier     Regex pattern
    lex2.Rule("WORD",        r"[a-zA-Z]+"),
    lex2.Rule("NUMBER",      r"[0-9]+"),
    lex2.Rule("PUNCTUATION", r"[.,:;!?\\-]")
]
lexer: lex2.ILexer = lex2.MakeLexer(ruleset=ruleset)

# Load input data by opening a file
lexer.Open(r"C:/path/to/file.txt")
# Or by directly passing a string
lexer.Load("The quick, brown fox jumps over 2 lazy dogs. \nMr. Jock, TV quiz PhD, bags few lynx.")

# Main lexing loop
token: lex2.Token
while(1):

    # Find the next token in the textstream
    try: token = lexer.GetNextToken()
    except lex2.excs.EndOfData:
        break

    info = [
         "ln: {}".format(token.position.ln +1),
        "col: {}".format(token.position.col+1),
        token.id,
        token.data,
    ]
    print("{: <12} {: <15} {: <20} {: <20}".format(*info))

lexer.Close()
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



## Contributing

The repository is hosted at [deltarazero/liblex2-py3](https://github.com/deltarazero/liblex2-py3) on GitHub. Contribution is always welcome; you can contribute by doing one of the following:

* __Submitting a pull request:__ to contribute your own changes to the repository. See ["About pull requests"](https://help.github.com/articles/about-pull-requests) for more information on pull requests on GitHub. Please follow the guidelines below:

    1. File an issue to notify the maintainers about what you're working on.
    2. Fork the repo, develop and test your code changes, add docs (if applicable).
    3. Make sure that your commit messages clearly describe the changes.
    4. Send a pull request.

    For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an issue to discuss your proposal first.

    Furthermore, maintaining your own fork of the repository is discouraged. Please submit pull requests instead, as this will make it less confusing for users to know which repository is the most up-to-date.

* __Submitting an issue:__ to report problems with the library, request a new feature, or to discuss potential changes before a pull request is created.



## License

© 2020-2021 DeltaRazero.
All rights reserved.

All included scripts, modules, etc. are licensed under the terms of the [zlib license](https://github.com/deltarazero/liblex2-py3/LICENSE), unless stated otherwise in the respective files.
