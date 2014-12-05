
# druid-cli

[Druid](http://druid.io/) data store does some incredible things and 
at the same time is a piece of software that can come in your
darkest nightmares.

It is simply hard to work with druid: starting from deploying
cluster and ending on using the simplest task.

*druid-cli* is a tool that aims to help with some tasks that
are really PITA in druid like:

* removing your data
* checking if anything works
* inspecting cluster

Project is still WIP so you should be aware that:
* some features are not available (tasks, removing segments etc.)
* it is very likely that error messages (or even stack traces)
  won't tell you what you're doing wrong

## Installation

Install from sources or use pip to fetch latest version
from PYPI:

    pip install druid-cli


## Usage

```
Usage: druid-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --overlord LOCATION     Hostname and port of overlord node
  --coordinator LOCATION  Hostname and port of coordinator node
  --broker LOCATION       Hostname and port of broker node
  --help                  Show this message and exit.

Commands:
  datasource  note: requires druid broker node
  rule        note: requires druid coordinator node
  server      note: requires druid coordinator node
  task        note: requires druid overlord node
```

druid-cli assumes that each type of druid nodes listens on
`localhost:8080`. This obviously can not be true so you have
give to `druid-cli` an explicit location of required druid node like:

    druid-cli --coordinator localhost:8082 datasource details
    
This obviuosly sucks but you can provide those locations using
following environment variables:

* `DRUID_OVERLORD`
* `DRUID_COORDINATOR`
* `DRUID_BROKER`

For more detailed usage on commands use `druid-cli <command> --help`

## Contributions

Contributions are very welcome.

## Changelist

### 0.2.0 (2014-12-05)
- support for submitting delete task

### 0.1.0 (2014-12-03)
- errors from druid API endpoints are now nicely formatted
- some errors can give hints about what is incorrect
  (currently only http 404 errors)
- `html2text` added to requirements
- initial tasks support (kill and noop)

## Licence

`druid-cli`  is licensed under LGPL license, version 3.
