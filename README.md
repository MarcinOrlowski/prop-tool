![prop-tool logo](artwork/prop-tool-logo.png)

# prop-tool #

`prop-tool` - Java *.properties file checker and syncing tool.

[master](https://github.com/MarcinOrlowski/prop-tool/tree/master):
[![Unit tests](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/prop-tool/branch/master/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/prop-tool)
[![Code lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml)

[dev](https://github.com/MarcinOrlowski/prop-tool/tree/dev):
[![Unit tests](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/MarcinOrlowski/prop-tool/branch/dev/graph/badge.svg?token=3THKJKSQ1G)](https://codecov.io/gh/MarcinOrlowski/prop-tool)
[![Code lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/linter.yml)
[![MD Lint](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml/badge.svg?branch=dev)](https://github.com/MarcinOrlowski/prop-tool/actions/workflows/markdown.yml)

This utility can be used to check your `*.properties` Java files to ensure correct syntax is used, all translation files are in sync
with base file, there are no missing keys or invalid punctuation and more. It can also create translation files adding missing keys
based on the content of base file.

```bash
$ prop-tool -b mark -l pl -v
Base: mark.properties
  Warnings: 1
    Brackets
      W: Line 3:16: No closing bracket for "<"
  PL: brackets_pl.properties
    Errors: 8, warnings: 3
      Sentence starts with different letter case.
        E: Line 8: "missingClosing" starts with lower-cased character. Expected UPPER-cased.
      Trailing white characters
        W: line 2: In comment: 2
        E: line 4: In "question" entry: 1
      Punctuation mismatch
        E: line 3: "exclamation" ends with " ". Expected "!".
        E: line 4: "newline" ends with "". Expected "\n".
      Bracket mismatch
        E: Line 2:1: "missingClosing": No closing bracket for "(".
        W: Line 3:16: No closing bracket for "<"
        E: Line 4:4: "missingOpening": No opening bracket matching ")".
      Quotation marks
        E: Line 12:5: "missingSingle": Quotation mark mismatch. Expected ", found `.
        E: Line 13:5: "remaining": Quotation mark mismatch. Expected ", found `.
        W: Line 14:11: No closing mark for ".
```

Based on `*.properties`
[file format docs](https://docs.oracle.com/cd/E23095_01/Platform.93/ATGProgGuide/html/s0204propertiesfileformat01.html).

## Checks ##

The main purpose of `prop-tool` is to ensure all property files are correct and that translation files are in sync with the
reference file. For that reason you need to have at least two `*.properties` files to use `prop-tool`. One is your base language
(usually English texts) used as reference and all the others are your translations. `prop-tool` performs several checks on both
base (reference) file and each translation.

For base file it executes following validators:

* Syntax: ensures use of allowed comment markers, key - value separators etc.
* Brackets: ensures all brackets opened are closed and there's no unpaired bracket.
* KeyFormat: ensures key string matches defined pattern.
* QuotationMarks: ensures all quotation marks are unpaired.
* TrailingWhiteChars: no trailing spaces nor tabs at the end of each line.
* TypesettingQuotationMarks: ensures that typesetting quotation marks (where you have separate quote opening and closing characters)
  are paired and properly nested.
* WhiteCharsBeforeLinefeed: ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`).

For translation files, the following checks are performed:

* Syntax: ensures use of allowed comment markers, key - value separators etc.
* Brackets: ensures all brackets opened are closed and there's no unpaired bracket.
* DanglingKeys: keys found in translation file but not present in base file.
* EmptyTranslations: empty translations for non-empty text in base file.
* FormattingValues: ensures all formatting values (i.e. `%s`, `%d`) present in base file are also present in translation, and the
  order is correct.
* KeyFormat: ensures key string matches defined pattern.
* MissingTranslation: keys found in base file, but missing in translation.
* Punctuation: ensures translation ends with punctuation mark (`:`, `.`, `?`, `!`) if entry in base file ends that way.
* QuotationMarks: ensures all quotation marks are unpaired.
* StartsWithTheSameCase: ensures translation starts with the same character case (upper/lower) as entry in base file.
* TrailingWhiteChars: no trailing spaces nor tabs at the end of each line.
* TypesettingQuotationMarks: ensures that typesetting quotation marks (where you have separate quote opening and closing
  characters) are paired and properly nested.
* WhiteCharsBeforeLinefeed: ensures there's no space nor tab character placed before linefeed literals (`\n` and `\r`).

NOTE: as this is quite common that translation file may not be updated instantly, `prop-tool` considers key presence condition
fulfilled also when given key exists in `B` file but is commented out and follow expected comment format:

```bash
# ==> KEY =
```

Default format can changed using `--tpl` argument.

If you want to ensure that all keys are in fact translated, use `--strict` mode while checking. When running with `--strict` option,
keys in commented out form are ignored.

## Installation ##

You can install `prop-tool` from [PyPi](https://pypi.org/project/prop-tool/):

```bash
pip install prop-tool
```

Alternatively, you can download `*.whl` archive and install it manually by issuing:

```bash
pip install --upgrade <FILE>.whl
```

You may also want to setup [virtual environment](https://docs.python.org/3/library/venv.html) first.

## Fixing files ##

You can use `prop-tool` to update your translation files by using `--fix` option. In such case `prop-tool` will completely rewrite
translation files, adding missing keys (in commented out form).

While content of written file is strongly based on base file Some normalization will be made

* There will be no more than one empty consequent empty line written,
* There will be no more than one consequent empty comment line (just comment marker) written.

NOTE: Be aware that `--fix` do NOT update existing translation file but builds it completely using base file as reference and
existing translations (if present). No other content of translation files (for example additional comments etc) will be preserved.

## Usage examples ##

Check if `de` translation of `test.properties` exists and is in sync:

```bash
prop-tool --base test.properties --lang de
```

You can omit `.properties` suffix in command line argument. NOTE: that file name must contain `.properties`
suffix, otherwise it will not be found:

```bash
prop-tool --base test --lang de
```

it will then look for `test_de.properties` file in the same folder `test.properties` resides and check it.

---

Check if `de`, `pl` and `fr` translations of `test.properties` and `gui.properties` exist and are in sync:

```bash
prop-tool --base test gui --lang de pl fr
```

it will then look for and validate following files

```bash
test_de.properties
test_pl.properties
test_fr.properties
gui_de.properties
gui_pl.properties
gui_fr.properties
```

---

Check if `es` translation of `gui.properties` is in sync and if there are any missing keys, rewrite translation file to contain all
keys from base:

```bash
prop-tool --base gui --lang es --fix
```

---

Check if `pt` translation of `gui.properties` is in sync and if there are any missing keys, rewrite translation file to contain all
keys from base using own comment format:

```bash
prop-tool --base gui --lang es --fix --tpl "COM >~=-> KEY SEP"
```

## Config file and command line arguments ##

You can use `prop-tool` by providing all required parameters directly from command line (see `--help`), or you can create
configuration file and use `--config` option to make `prop-tool` load it and use. Almost all options can be set in configuration
files, which helps, for example using `prop-tool` as part of CI/CD or GitHub Actions.

Configuration file is plain text file, following [INI file format](https://en.wikipedia.org/wiki/INI_file) and can be created
using any text editor. Please see commented [config.ini](config.ini) for example configuration file and all available options.

> NOTE: when using configuration file and command line arguments, the order of precedence is this:
> * default configuration goes first,
> * if config file is given and can be loaded and parsed, then it overrides default configuration,
> * if there's any command but line argument `--config` specified, then it overrides whatever is is set in config file.
> 
> For example:
> * by default, `verbose` option is off
> * your config file sets `verbose = true`, enabling verbose output,
> * but your invocation is `prop-tool --config config.ini --no-verbose`, therefore `verbose` mode is set `OFF`.

## Limitations ##

* As of now `prop-tool` do not handle multiline entries.
* `FormattingValues` check will do not support positional placeholders, formats using space leading positive numbers.
* `TypesettingQuotationMarks` is not covering all possible pairs yet due
  to [limitations of current implementation](https://github.com/MarcinOrlowski/prop-tool/issues/19).

## License ##

* Written and copyrighted &copy;2021 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* prop-tool is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)
