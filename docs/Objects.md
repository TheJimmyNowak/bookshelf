# List of all objects in app

## Book

* img
* name
* author
* price
* condition
* user:
    - name
    - id (link to user site)

## User

* name
* localization
* mail
* phone
* added books:
    - name
    - id (link to book site)

## Chat

* books_offered: [
    - name
    - author
    - img
    - condition
      ]

* seller_book:
    - name
    - author
    - img
    - condition

* chat history:
    - message:
        - content
        - date
        - author