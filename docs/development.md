# Development

## Unit Tests

Most of the unit tests are proper unit tests, e.g. they don't need human interaction to run. However, the tests that test the GPG signing need a human to type in the password for the GPG key to be used. The key that is used in the tests is generated specifically for the tests. Therefore, do not type your own GPG's password, but the password written below.

We abstained from simplifying this by automating the input of the GPG key or by using an empty password. This project encourages proper usage of encryption techniques and as such also wants to encourage the creation and usage of a real GPG key with a secure password.

### Normal Unit Tests (non-interactive)

Run all (non-interactive) unit tests in `src`:

```
python3 -m unittest *_test.py
```

### Interactive Unit Tests

Run interactive unit tests in `src`:

```
python3 -m unittest *_test_interactive.py
```

When prompted, type in the password `Test123`.

## Pylint

I try to conform to:

```
pylint3 --indent-string='  ' --disable=duplicate-code
```
