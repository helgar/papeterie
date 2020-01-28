# A guide to Customization

I encourage the use of my scripts for making your own wedding stationery. Here's the easiest way to achieve that.

If you have feedback for me, please contact me.

## Look at the examples

I provided a bunch of [examples](examples.md) of various stationery. It is probably easiest to pick what is closest do your plan and copy the folder to `data/myexample`.

## Format the tex template

The `papeterie.tex` file is a normal tex file, with these exceptions:

*  It contains ALL CAPS placeholders for all text snippets that are formatted individually.
*  For included pictures, the path of the pictures are prefixed with PAPETERIEPICPATH

To customize this:

*  Replace the placeholders and picture paths with real text and paths to real pictures (or use the ones in the folder)
*  Change the template as you see fit
*  Run pdflatex on the file
*  Repeat till you are happy with the result
*  Finally, copy all pictures you are using into the folder, add placeholders where individual texts come in and put the magic PAPETERIEPICPATH back


## Assemble the recipient file

Create a CSV file with your recipient's data. One recipient per line. The first line are the colum names.

Create and fill columns for all data that you need (like the names, address etc.) and all "switches" that you want individualize the text on. For example if you want to create texts in different languages, there should be a "Language" column.

Note: It is tedious to create CSV files in a text editor. We recommend using a spread sheet software (LibreOffice, Excel, Google Sheets) and export to CSV.

## Create jinja2 templates

For each individually-formatted text snippet in the stationery, create/copy a jinja2 template. In the jinja2 template write the text you want and use the colum names from the CSV file for switches.

For example if you want texts in different languages, your snippet should contain something like

```
{% if Language=German %}Liebe {% Name %}{% else %}Dear {% Name %}{% end if %} ...
```

Refer to the [jinja](https://jinja.palletsprojects.com/) documentation.

## (Optionally) Create a valid GPG key

If you want to use the GPG/PGP signing feature, you should install `gpg2` and create a valid GPG key.

Note: it is most romantic for a wedding stationery to generate a common key for a common email addres for the individuals getting married.

## Create the config file

The config file must be named `config.json` and be formatted in JSON (d'uh).

It contains these things:

*  A dictionary mapping the ALL CAPS snippets names from the tex template to the filenames of the jinja2 templates that are use to generate those text snippets.
*  (Optionally) A dictionary mapping the ALL CAPS snippet names of the signed snippets mapping to the ALL CAPS snippet names of the original snippet.

