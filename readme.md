<div align="center">
<h1>Specialty Referral Network</h1>
</div>

<!-- <p align="center">
    <strong>demesstify</strong> is a Python library that demystifies your messages and allows for easy analysis and visualization of conversations.
</p> -->

<hr>

## Table of contents

<!-- * [Main features](#main-features) -->
* [Getting set up](#getting-set-up)
    * [Dependencies](#dependencies)
    * [Installing the dependencies](#installing-the-dependencies)
* [Starting the web application](#starting-the-web-application)
* [Visualizing data](#visualizing-data)
    * [Input formatting](#input-formatting)
* [Future improvements](#future-improvements)
* [Authors](#authors)

<!-- ## Main features

Here are just a few things that this project can do:
* Read message data from various sources, including your local iMessages database, a [Tansee](https://www.tansee.com) text file, or some randomly generated dummy text
* Perform text analysis on your messages so you can see things like the average number of texts received per day or the most number of messages that were sent in a row
* Analyze which emojis or reactions (if you're using iMessage) were most frequently used, among other thing
* Perform sentiment analysis on your messages to see the polarity of your conversations
* Calculate statistics about the attachments you exchanged (if you're using iMessage)
* Generate tailored visualizations such as word clouds or a radial heatmap that plots hour of the day against day of the week -->

## Getting set up

The source code can be viewed on GitHub [here](https://github.com/jakebrehm/referral-network).

### Dependencies

This project currently requires a minimum of Python 3.10.

<!-- This project currently requires a minimum of Python 3.10 and depends on the following packages:

| Package                                                | Description                           |
| ------------------------------------------------------ | ------------------------------------- |
| [pandas](https://github.com/pandas-dev/pandas)         | For easy manipulation of message data | -->

<!-- plotly, flask -->

### Installing the dependencies

```
cd path\to\clone\repository\to
```

```
git clone https://github.com/jakebrehm/referral-network.git
```

```
pip install poetry
```
or `python3` if you also have Python 2 installed on your machine (this is typically the case by default for certain operating systems like MacOS).

```
poetry install
```

## Starting the web application

```
poetry shell
```

```
python referral_network/app.py
```

## Visualizing data

### Input formatting

- Must be in *CSV* format
- Must only include three columns:
    - One including the referring department
    - Another including the department being referred to
    - Finally, a column containg the number days to schedule

## Future improvements

- Implement a memory of the visualization settings between sessions
- Added more customizability to the visualization via the sidebar

## Authors

- **Jake Brehm** - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)
- **Sayan Swar** - [Email](mailto:sayankrswar@hotmail.com) | [Github](http://github.com/skswar) | [LinkedIn](http://linkedin.com/in/sayankrswar)