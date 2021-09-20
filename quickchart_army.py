from quickchart import QuickChart


def get_quickchart(troop_datas: list, troop_labels: list):
    qc = QuickChart()
    qc.background_color = 'transparent'
    qc.config = {
        'type': 'doughnut',
        'data': {
            'datasets': [
                {
                    'data': troop_datas,
                },
            ],
            'labels': troop_labels,
        },
        'options': {
            'plugins': {
                'datalabels': {
                    'color': 'white',
                    'backgroundColor': '#404040',
                    'borderRadius': 3,
                },
                'doughnutlabel': {
                    'labels': [{
                        'color': 'white',
                        'text': sum(troop_datas),
                        'font': {
                            'size': 20,
                            'weight': 'bold'
                        }
                    }, {
                        'text': 'total',
                        'color': 'white',
                    }]
                }
            },
            'legend': {
                'labels': {
                    'fontColor': "white",
                }
            },
        }
    }

    return qc.get_short_url()


if __name__ == '__main__':
    url = get_quickchart([1, 2, 3, 4], ['test1', 'test2', 'test3', 'test4'])
    print(url)
