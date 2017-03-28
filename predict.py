import pandas as pd
import random
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datetime

def engine_usage():

    eng4 = [64225, 18448, 6620]
    eng5 = [62908, 21710, 4675]
    eng6 = [48399, 23209, 17685]
    raw_data = {'state': ['On', 'Off', 'Transition'],
                'Engine 4': [x * 100 / sum(eng4) for x in eng4],
                'Engine 5': [x * 100 / sum(eng5) for x in eng5],
                'Engine 6': [x * 100 / sum(eng6) for x in eng6]}

    df = pd.DataFrame(raw_data, columns=['state', 'Engine 4', 'Engine 5', 'Engine 6'])

    pos = list(range(len(df['Engine 4'])))
    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10, 5))

    # Create a bar with pre_score data,
    # in position pos,
    plt.bar(pos,
            # using df['pre_score'] data,
            df['Engine 4'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            # with label the first value in first_name
            label=df['state'][0])

    # Create a bar with mid_score data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos],
            # using df['mid_score'] data,
            df['Engine 5'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#F78F1E',
            # with label the second value in first_name
            label=df['state'][1])

    # Create a bar with post_score data,
    # in position pos + some width buffer,
    plt.bar([p + width * 2 for p in pos],
            # using df['post_score'] data,
            df['Engine 6'],
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#FFC222',
            # with label the third value in first_name
            label=df['state'][2])

    # Set the y axis label
    ax.set_ylabel('%')
    ax.set_xlabel('Engine State')

    # Set the chart's title
    ax.set_title('Engine Usage')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['state'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos) - width, max(pos) + width * 4)
    plt.ylim([0, 100])
    #plt.ylim([0, max(df['Engine 4'] + df['Engine 5'] + df['Engine 5'])])

    # Adding the legend and showing the plot
    plt.legend(['Engine 4', 'Engine 5', 'Engine 6'], loc='upper right')
    plt.grid()
    plt.show()

def stable_state():

    def get_time(record):
        print(str(record.split()[1]))
        return record.split()[1]

    input_file = "July/sfoc/filled/03.csv"
    df = pd.read_csv(input_file).head(300)
    sfoc = df.SFOE5SFOC
    time = map(get_time, df.timestamp_selected)

    datetimes = [datetime.datetime.strptime(t, "%H:%M:%S").time() for t in time]

    fig = plt.figure()
    prop = {'weight' : 'bold', 'size': 15}

    ax = fig.add_subplot(111)
    ax.set_title('Stable state - Engine 5', prop)
    ax.set_xlabel('Time', {'size': 15})
    ax.set_ylabel('SFOC', {'size': 15})


    plt.plot(datetimes, sfoc, color = '#F78F1E')
    plt.show()


if __name__ == "__main__":
    #engine_usage()
    stable_state()
