# Just Type
Just Type is an offline, minimalist typing speed test application built with Tkinter.

It is loosely based the site [10fastfingers](http://10fastfingers.com/typing-test/english), using similar wordbanks for the 'easy' and 'advanced' tests.

![Just Type](http://i.imgur.com/YS79Jk2.gif)

## Features
* Visual feedback for words that have been typed and are currently being typed
* Live WPM (words per minute) or CPM (characters per minute) display
* 3 types of timed randomly-generated tests, including one using the NumPad
* Top 10 fastest times for each test, including their dates and your accuracy
* Resettable graphs showing WPM/CPM progress over time for each test
* Submit your own text for a customized test that ends when you're done typing it

<p align="center">
  <img src="http://i.imgur.com/SHWOUrI.png" alt="Highscores" width="400"/>
</p>

## Requirements

Just Type utilizes matplotlib to create graphs, so make sure you have that installed. If on Windows-

```
python -m pip install -U pip setuptools
python -m pip install matplotlib
```

More info can be found on the [matplotlib installation site](https://matplotlib.org/users/installing.html).

## Usage

To launch Just Type, simply run `__main__.pyw` and have fun!

<p align="center">
  <img src="http://i.imgur.com/sGglfSM.png" alt="Submit Custom" width="400"/>
</p>

## Built With

* [Tkinter](https://wiki.python.org/moin/TkInter) - GUI package used
* [matplotlib](https://matplotlib.org/) - Python 2D plotting library

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

<p align="center">
  <img src="http://i.imgur.com/xmZ6wzu.png" alt="Submit Custom" width="400"/>
</p>
