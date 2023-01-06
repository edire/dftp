# Description

A Python library by Dire Analytics for custom FTP connections.

## Installation

pip install git+https://github.com/edire/dftp.git

## Usage

```python
import dftp

ftp_con = dftp.SFTP()
ftp_con.get({source_filepath}, {destination_filepath})
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Updates

01/06/2023 - Removed stat dependency.