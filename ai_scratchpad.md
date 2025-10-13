## Polishing to satisfaction

* the 'threads' panel should be in a row with the text display, on its left, but is currently stacked on top

* Refactor the `run_single_turn()` call to be asynchronous using a Textual `@work` decorator.

* While the simulation is processing, display a `LoadingIndicator` and temporarily disable the "Next Turn" button.

* Wrap the call to the simulation engine in a try/except block. If the simulation raises an error, display it cleanly in the `RichLog` instead of crashing the TUI.

* Re-introduce the `Input` widget from the reference app, but keep it disabled for now. This reserves a space for future interactive commands.

* It seems some of the colors and formatting have regressed from @ext_docs/textual_reference_app/chat_app.py, so let's brush up the styling; note that there is a scss file in that directory

* Not an issue, but I noticed we're writing to 'RichLog'; how do I see those messages?

* Just curious, do we have any configuration we can do to tweak how the text displays? (like padding or something)
