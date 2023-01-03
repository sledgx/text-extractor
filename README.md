# text-extractor

Text extractor from documents as a service.

## About the service

The service allows you to extract text from documents in PDF, DOC, DOCX and ODT formats.

## How to use

All of the following examples will bring you the service on `http://localhost:8080`.

### Basic usage

This will run the service with the default option:

```sh
docker run -d \
    --name text-extractor \
    -p 8080:80 \
    sledgx/text-extractor
```

### Usage with custom parameters

You can define log verbosity and maximum document size in the environment variables `LOG_LEVEL` and `MAX` respectively:

```sh
docker run -d \
    --name text-extractor \
    -e LOG_LEVEL=debug \
    -e MAX_FILE_SIZE=15MB \
    -p 8080:80 \
    sledgx/text-extractor
```

The values accepted by `LOG_LEVEL` are `error`, `warning`, `info`, `debug` and `notset`, default is `info`.

the value of `MAX_FILE_SIZE` must be specified in human-readable format, i.e. the value followed by the unit of measurement (`B`, `KB`, `MB`, `GB` or `TB`).

## How to make service requests

The service exposes a single endpoint for text conversion.

### Convert

With this method you can upload a document and receive the text contained in it as output.
You can also specify whether to use the OCR system for extracting text from images, useful for documents in PDF format:

```sh
curl -X POST http://localhost:8080/convert \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@path.ext' \
    -F 'ocr_fallback=true'
```

or

```sh
curl -X POST http://localhost:8080/convert \
    -H 'Content-Type: multipart/form-data' \
    -H 'x-ocr-fallback: true' \
    -F 'file=@path.ext'
```

## License

Released under the [MIT License](https://github.com/sledgx/text-extractor/blob/master/LICENSE).
