
How To Run Comands
----------------

- Install only one requirement:

    ```bash
    pip3 install django
    ```

- For generate code in JSON file run command in /codegen/ folder:

  ```bash
  python manage.py generate_codes -amount your_amount -group your_group_name
  ```

Note: if needed, command also got '-file_name' flag for customize file path.


- For run test in /codegen/ folder:

    ```bash
     python manage.py test
    ```

