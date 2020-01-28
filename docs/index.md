# Documentation of Helga's Papeterie

This is a set of scripts which generate beautiful and secure stationery, for example for wedding invitations, save-the-date cards and thank-you cards.

Features are:
*  Option to PGP/GPG-sign the card's text.
*  Different themes depending on the recipient (like the normal one for your parents, the Cthulhu version for your role-playing group, the goth version for your friends of the night, etc.
*  Rendering of individual texts considering singular/plural, language, level of formality, friendship status, whether or not they are invited to the ceremony or not, whether or not they are out of town.
*  Fully customizable latex layout.

## Usage

In `src`:

```
python3 serial.py --recipient_file=../data/example_recipients.csv --input_dir=../data/example_savethedate_card --output_file=/tmp/papeterie.pdf
```

See the [Examples](examples.md) for the various options, including example_savethedate_card_signed for a signed save-the-date card.

## Details

*  [Installation](installation.md): what is needed to run papeterie.
*  [Architecture](architecture.md): an overview of the architecture.
*  [Customization](customization.md): a guide how to customize papeterie for your needs.
*  [Examples](examples.md): a description of the example pieces of papeterie.

## Contact

If you have any questions, contact me via email:

*  helga@velroyen.de
*  PGP Key: 2842DF996EEA9318
*  Fingerprint: CB79 DA03 6022 B951 5047  865A 2842 DF99 6EEA 9318

### Customizations and images on demand

If you want a particular customization (including custom drawings), send me a request with an offer.

### Pizza

If you like what I did and want to buy me a pizza: [paypal.me/HelgaVelroyen](http://paypal.me/HelgaVelroyen)
