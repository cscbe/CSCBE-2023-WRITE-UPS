# CTFserver

CTFserver is a multi-threaded _TCP Server_ for all CTF makers.
This server will be updated constantly.
<br />
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9f1b0d2bdc0b43a78ddfacd0e7d7d079)](https://www.codacy.com/gh/OussamaMater/CTFServer/dashboard?utm_source=github.com&utm_medium=referral&utm_content=OussamaMater/CTFServer&utm_campaign=Badge_Grade)

<img src="https://i.ibb.co/VBCQNwT/120859501-3315221428599513-5673978447987533463-n.png" alt="120859501-3315221428599513-5673978447987533463-n" border="0">

## Author

Oussama Mater

[<img align="left" alt="oussamamater.github.io" src="https://img.icons8.com/color/48/000000/geography.png" />][website]
[<img align="left" alt="OussamaMater | Twitter" src="https://img.icons8.com/color/48/000000/twitter.png" />][twitter]
[<img align="left" alt="OussamaMater | LinkedIn" src="https://img.icons8.com/color/48/000000/linkedin.png" />][linkedin]
[<img align="left" alt="OussamaMater | Instagram" src="https://img.icons8.com/color/48/000000/instagram-new.png" />][instagram]
[<img align="left" alt="OussamaMater | Facebook" src="https://img.icons8.com/color/48/000000/facebook-new.png" />][facebook]

<br /><br />

## Installation && Usage

Requirements: _Python_ 3.x should be fine.

```bash
git clone https://github.com/OussamaMater/CTFServer.git
cd CTFServer
pip3 install -r requirements.txt
python3 server.py
```

_Note: Flask will be installed, if you have an env set for that please switch to it._

You can mark it as an excutable and run it;

```bash
chmod +x server.py
./server.py
```

For more details on the usage execute with --help/-h flag;

```bash
./server.py -h
```

_Note: Soon the server will be added as a pip package._

## Update

This server will receive changes, to keep it up-to-date;

```bash
cd path/to/CTF_SERVER
git pull origin master
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

    - TODO:
        - Create a GUI app using Flask (branch: feature).

## Fun Fact

The server was initially coded for the sake of demonstrating socket's workflow to my girl.

## License

[MIT](https://choosealicense.com/licenses/mit/)

<br />

[website]: https://oussamamater.github.io
[twitter]: https://twitter.com/OussamaMater
[instagram]: https://www.instagram.com/oussama_ma09/
[linkedin]: https://www.linkedin.com/in/oussama-mater-154465198/
[facebook]: https://www.facebook.com/oussama.mater.3/
