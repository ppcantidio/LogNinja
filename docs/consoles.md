---
hide:
  - navigation
---
# Consoles

## About
Consoles are objects that handle logs to stderr. They are responsible for applying effects if necessary, and in some cases, handling exceptions. Consoles are a concept inherited from Rich. You can also set a Rich Console as your custom Console, but keep in mind that your console will only be called by three functions, which follow this interface:

You can also create your own custom console.

## LogNinja Consoles
LogNinja provides two consoles that can be used to manage your logs: `logninja.consoles.NinjaConsole` and `logninja.consoles.NinjaRichConsole`. They doesn't receive any parameters upon initialization and are used by `LogConsoleConfig`.

### NinjaConsole
`logninja.consoles.NinjaConsole` is a simple console, recommended for use in cloud environments. It doesn't have any style or color applied and is designed to be simple and easy to read by observability systems.
#### Examples:
Combined with `NinjaJsonFormatter`:
```
sdfsdfsd
```
Combined with `NinjaFormatter`:
```
sdfsdfsd
```


### NinjaRichConsole
`logninja.consoles.NinjaRichConsole` is a console based on `Console` from `rich`. To use this console, you need `rich` as a dependency in your project. You can get it using `pip install rich` or `pip install logninja[rich]`. This will provide powerful, colorful logs and pretty exceptions.

#### Examples:
Combined with `NinjaJsonFormatter`:
```
sdfsdfsd
```
Combined with `NinjaFormatter`:
```
sdfsdfsd
```