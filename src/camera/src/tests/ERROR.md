This error was rised during `pip3 install -r reqirements-dev.txt`:

```
WARNING: The scripts py.test and pytest are installed in '/home/frederik/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  ```

It's better to run `$ python3 -m pytest` instead of `$ pytest` anyways, so this should not be an issue.
