# ep

A tool to support an explicit contract between application and plaftorm.

Inspired by Heroku's post about [an explicit contract between application and
platform](https://blog.heroku.com/archives/2011/6/28/the_new_heroku_4_erosion_resistance_explicit_contracts),
`ep` aims to provide a reusable mechanism to cover that contract.

As a summary, Heroku's contract is based on:

- Dependency management: declared as part of the codebase
- Procfile: as a mechanism to specify what should be run
- Web process binds to $PORT (an externally provided environment variable
- stdout for logs
- Resource handles in the environment: environment variables for configuration,
  in particular for connecting to external resources


## What defines a contract in `ep`

An `ep`-based contract tries to cover these areas:

- A defined way to specify your dependencies
- A defined way to run your project
- Configured purely via environment variables

The particulars of the contract are specified via a configuration file that
lives on the root of your application's repository. This configuration file
is in YAML format and is called `ep.yml` by default.


### A defined way to specify dependencies

Dependencies can be of various types. `ep` aims to cover at least the
following:

 - `python`: via pip install of a requirements file. Defaults to
   `requirements.txt` at the root folder
 - `node`: via npm install of a package file. Defaults to `package.json` at
   the root

> The root here refers to the directory where `ep.yml` lives.

> Future extensions may cover ruby gems, bower packages, and even os-level
> packages on some OSes

There are two types of dependencies from the PoV of `ep`:
 - Those that the tool will be able to install
 - Those that it will only verify, but not attempt to install. These include
   e.g. the version of Python in your system

Some of these dependencies will have their defaults.
This could be a partial example of a `ep.yml`.

```yaml
ep: 1.0.0
dependencies:
  - python
      version: 2.7
      file: requirements/runtime.txt
  - npm
```

The command to install dependencies via ep is:

    ep setup

`ep` will always install dependencies in an isolated environment. This means
e.g. a virtual environment in Python, local npm install etc. `ep` will manage
the creation of this isolated environment for you.


### A defined way to run your project

`ep` doesn't force you to use `Procfile`, but lets you define your run
command:

```yaml
run: gunicorn myapp.wsgi
```

Defaults to running a `Procfile` in your root.

Run your project using:

    ep run


### Configuration via environment variables

Your app should be configurable via environment variables. Your `ep.yml` file
provides an explicit definition of what those variables are, and optional
default values and help.

```yaml
run:
  environment:
    PORT:
      default: 8000
      help: The port the web application will run on
    SOME_EXTERNAL_SERVICE_URL:
      default: http://localhost:9000
```

`ep run` will complain if variables that do not have a default value are not
privided, and refuse to run.


## Additional features

Besides the basic explicit contract defined above, `ep` helps you with extra
things.

### Extra setup steps

TODO: define a mechanism to have additional setup steps such as running
migrations on a django project, etc...
