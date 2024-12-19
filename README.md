# Keyset pagination example

## Install dependencies:
```bash
make deps
```

## Request for offset example:
```
http://0.0.0.0:8000/offset-example?page_size=100&offset=1900000
```

## Request for keyset example:
```
http://0.0.0.0:8000/keyset-example?page_size=100&last_item_sorting_value=2020-12-22T16:42:58.003807
```
