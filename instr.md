For all the Python scripts importing 

import helpers.hselect_action

use the following pattern for processing the actions

_VALID_ACTIONS = ["download", "process", "upload", "cleanup"]
_DEFAULT_ACTIONS = ["download", "process", "upload"]

def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(...)
    # Define valid and default actions.
    hselacti.add_action_arg(parser, VALID_ACTIONS, _DEFAULT_ACTIONS)
    hparser.add_verbosity_arg(parser)
    return parser

def _main(args: argparse.Namespace) -> None:
    # Select which actions to execute.
    actions = hselacti.select_actions(
        args,
        valid_actions=VALID_ACTIONS,
        default_actions=_DEFAULT_ACTIONS,
    )
    print(hselacti.actions_to_string(actions, VALID_ACTIONS, add_frame=True))
    # Execute selected actions.
    while actions:
        action = actions[0]
        to_execute, actions = hselacti.mark_action(action, actions)
        if not to_execute:
          continue
        if action == "download":
            data = _download()
        elif action == "process":
            data = _process(...)
        elif action == "upload":
            _upload(...)
        elif action == "cleanup":
            _cleanup()
        else:
            raise ValueError(f"Invalid action='{action}'")
     hdbg.dassert_eq(len(actions), 0,
       "There are unprocessed actions: %s", str(actions))

