# mdmail

A tool to send mails written in Markdown

## Example

```sh
docker run --rm --interactive roy2220/mdmail:v0.2.0 \
    --smtp-host=smtp.mail.com \
    --smtp-port=465 \
    --smtp-pass=MY_PASSWORD \
    from@mail.com \
    to@mail.com \
    'My Subject' \
    - < ./my_mail.md
```

## Usage

```
usage: mdmail [-h] [-H HOST] [-p PORT] [-u USER] [-P PASS] [-a FILE] FROM TO SUBJECT FILE

positional arguments:
  FROM                  the sender of the mail
  TO                    the recipients of the mail (separated by commas)
  SUBJECT               the subject of the mail
  FILE                  the markdown file as the content of the mail

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --smtp-host HOST
                        specify the host of smtp server (default: 127.0.0.1)
  -p PORT, --smtp-port PORT
                        specify the port of smtp server (default: 465)
  -u USER, --smtp-user USER
                        specify the user of smtp server. if not specified, the
                        sender will be used instead (default: None)
  -P PASS, --smtp-pass PASS
                        specify the password for the user of smtp server
                        (default: None)
  -a FILE, --attachment-file FILE
                        specify the attachment file (default: None)
```
