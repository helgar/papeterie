# Architecture

Here's a wild drawing of the architecture.

[Drawing](https://docs.google.com/drawings/d/1Q_zDW5VV70Ye2TqWc3QtPtH_Ir_GIL2Tirx8WK3nKpA/edit?usp=sharing)

The script serial.py executes the following steps:

*  Read a list of recipient data from a CSV file.
*  Render a bunch of text snippets by filling jinja2 templates with the recipient data.
*  Optionally, sign the text with a GPG key.
*  Insert the rendered text snippets into a tex template.
*  Generate a pdf per recipient by running pdflatex on the tex template.
*  Merge the individual pdfs into one.

These data must be provided to the script:

*  A CSV file with the recipients' data
*  A folder containing a configuration file (JSON), a bunch of jinja2 snippets, a tex template.
*  (Optionally) If you want to use the GPG-signing feature, you need to have gpg2 set up with a key ready to use.

## The recipient CSV file

The CSV file should comply to the following:

*  One line per recipient.
*  The first line contains column names.
*  The column names can be chosen arbitrarily, but should not be empty. (Probably also not contain funny stuff like umlauts.)
*  The column names will be reused in the jinja2 template, so choose something meaningful.

## The configuration file

The config file must be called `config.json`. It contains:

*  A dictionary mapping snippet names to jinja2 template files.
*  (Optionally) A dicitionary mapping snippet names of snippets containing signed messages, mapping to the snippet name of the original message.

The snippet names should be ALL CAPS words that are not substrings of each other, e.g. avoid "MESSAGE" and "SIGNEDMESSAGE", but chose "MESSAGE" and "SIGNEDMSG".

## The jinja2 snippet templates

For each section that you want to format and customize individually in the stationery, you should create a separate jinja2 template. The template should render the individual texts given the data of one recipient.

For example such text snippets of a save-the-date card could be:

* The post address of the receipient
* The text on the back of the card

If you want the front of the card to look the same for everyone (like the same picture and title "Save the Date" for example), you don't need a jinja template for that.

## The signing of text snippets

Optionally, the text snippets can be GPG/PGP sigend. For that, they will be written to disk and signed with gpg2 using the key which you specified with the key id.

## Tex Template

Provide a tex file, which has placeholder where the text snippets are inserted. The placeholders must be the ALL CAPS snippet names mentioned above.
