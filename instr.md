- Change the 
## Print Variable Name With Value
- When using `print()` to inspect a variable, always include the variable name as a
  label alongside its value
  ```python
  print("type(env)=", type(env))
  print("env=", env)
  ```
  - **Bad**: bare output with no context
    ```python
    print(env)
    ```
  - **Good**: self-documenting print with variable name
    ```python
    print("env=", env)
    ```
