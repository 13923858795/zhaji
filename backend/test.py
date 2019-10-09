# def normalize_card_number(card_number):
#     """如果 card_number 大于8位, 则将10进制的卡号, 转化为16进制, 并取其后六位, 最后用0补
#   全为8位大写16进制. 否则将其转换为8位大写16进制
#
#   Arguments:
#       card_number {int|string} -- 卡号
#
#   Returns:
#       str -- 处理后的卡号
#   """
#     card_number = str(card_number).strip()
#
#     if len(card_number) > 8:
#         card_number = hex(int(card_number))[-6:]
#
#     return card_number.upper().rjust(8, "0")
#
#
# card_number = '0956644423'
# a = normalize_card_number(card_number)
#
# print( a)

a = {
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 563,
  "links": [],
  "panels": [
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 7,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 2,
      "links": [],
      "options": {
        "displayMode": "lcd",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "orange",
                "value": 60
              },
              {
                "color": "red",
                "value": 80
              }
            ],
            "unit": "decgbytes"
          },
          "override": {},
          "values": false
        },
        "orientation": "vertical"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "alias": "sda1",
          "refId": "A",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda2",
          "refId": "B",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda3",
          "refId": "C",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda4",
          "refId": "D",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda5",
          "refId": "E",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda6",
          "refId": "F",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda7",
          "refId": "G",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda8",
          "refId": "H",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda9",
          "refId": "I",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda10",
          "refId": "J",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda11",
          "refId": "K",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda12",
          "refId": "L",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda13",
          "refId": "M",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda14",
          "refId": "N",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda15",
          "refId": "O",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda16",
          "refId": "P",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "",
      "transparent": true,
      "type": "bargauge"
    },
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 10,
        "w": 16,
        "x": 0,
        "y": 7
      },
      "id": 4,
      "links": [],
      "options": {
        "displayMode": "gradient",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "decimals": null,
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "blue",
                "value": null
              },
              {
                "color": "green",
                "value": 20
              },
              {
                "color": "orange",
                "value": 40
              },
              {
                "color": "red",
                "value": 80
              }
            ],
            "unit": "celsius"
          },
          "override": {},
          "values": false
        },
        "orientation": "horizontal"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "alias": "Inside",
          "refId": "H",
          "scenarioId": "csv_metric_values",
          "stringInput": "100,100,100"
        },
        {
          "alias": "Outhouse",
          "refId": "A",
          "scenarioId": "random_walk"
        },
        {
          "alias": "Area B",
          "refId": "B",
          "scenarioId": "random_walk"
        },
        {
          "alias": "Basement",
          "refId": "C",
          "scenarioId": "random_walk"
        },
        {
          "alias": "Garage",
          "refId": "D",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "Gradient mode",
      "type": "bargauge"
    },
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 10,
        "w": 6,
        "x": 16,
        "y": 7
      },
      "id": 6,
      "links": [],
      "options": {
        "displayMode": "basic",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "decimals": null,
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "blue",
                "value": null
              },
              {
                "color": "green",
                "value": 42.5
              },
              {
                "color": "orange",
                "value": 80
              },
              {
                "color": "red",
                "value": 90
              }
            ],
            "unit": "watt"
          },
          "override": {},
          "values": false
        },
        "orientation": "horizontal"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "refId": "H",
          "scenarioId": "csv_metric_values",
          "stringInput": "100,100,100"
        },
        {
          "refId": "A",
          "scenarioId": "random_walk"
        },
        {
          "refId": "J",
          "scenarioId": "random_walk"
        },
        {
          "refId": "K",
          "scenarioId": "random_walk"
        },
        {
          "refId": "L",
          "scenarioId": "random_walk"
        },
        {
          "refId": "M",
          "scenarioId": "random_walk"
        },
        {
          "refId": "N",
          "scenarioId": "random_walk"
        },
        {
          "refId": "O",
          "scenarioId": "random_walk"
        },
        {
          "refId": "P",
          "scenarioId": "random_walk"
        },
        {
          "refId": "Q",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "Basic",
      "type": "bargauge"
    },
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 22,
        "w": 2,
        "x": 22,
        "y": 7
      },
      "id": 8,
      "links": [],
      "options": {
        "displayMode": "lcd",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "red",
                "value": null
              },
              {
                "color": "red",
                "value": 90
              }
            ]
          },
          "override": {},
          "values": false
        },
        "orientation": "vertical"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "refId": "A",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "Completion",
      "type": "bargauge"
    },
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 12,
        "w": 22,
        "x": 0,
        "y": 17
      },
      "id": 10,
      "links": [],
      "options": {
        "displayMode": "gradient",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "blue",
                "value": null
              },
              {
                "color": "green",
                "value": 30
              },
              {
                "color": "orange",
                "value": 60
              },
              {
                "color": "red",
                "value": 80
              }
            ],
            "unit": "decgbytes"
          },
          "override": {},
          "values": false
        },
        "orientation": "vertical"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "alias": "sda1",
          "refId": "A",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda2",
          "refId": "B",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda3",
          "refId": "C",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda4",
          "refId": "D",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda5",
          "refId": "E",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda6",
          "refId": "F",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda7",
          "refId": "G",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda8",
          "refId": "H",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda9",
          "refId": "I",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda10",
          "refId": "J",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda11",
          "refId": "K",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda12",
          "refId": "L",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda13",
          "refId": "M",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda14",
          "refId": "N",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda15",
          "refId": "O",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda16",
          "refId": "P",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "",
      "type": "bargauge"
    },
    {
      "datasource": "gdev-testdata",
      "gridPos": {
        "h": 8,
        "w": 24,
        "x": 0,
        "y": 29
      },
      "id": 11,
      "links": [],
      "options": {
        "displayMode": "basic",
        "fieldOptions": {
          "calcs": [
            "mean"
          ],
          "defaults": {
            "mappings": [],
            "max": 100,
            "min": 0,
            "thresholds": [
              {
                "color": "blue",
                "value": null
              },
              {
                "color": "green",
                "value": 30
              },
              {
                "color": "orange",
                "value": 60
              },
              {
                "color": "red",
                "value": 80
              }
            ],
            "unit": "decgbytes"
          },
          "override": {},
          "values": false
        },
        "orientation": "vertical"
      },
      "pluginVersion": "6.4.0-beta2",
      "targets": [
        {
          "alias": "sda1",
          "refId": "A",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda2",
          "refId": "B",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda3",
          "refId": "C",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda4",
          "refId": "D",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda5",
          "refId": "E",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda6",
          "refId": "F",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda7",
          "refId": "G",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda8",
          "refId": "H",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda9",
          "refId": "I",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda10",
          "refId": "J",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda11",
          "refId": "K",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda12",
          "refId": "L",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda13",
          "refId": "M",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda14",
          "refId": "N",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda15",
          "refId": "O",
          "scenarioId": "random_walk"
        },
        {
          "alias": "sda16",
          "refId": "P",
          "scenarioId": "random_walk"
        }
      ],
      "timeFrom": null,
      "timeShift": null,
      "title": "",
      "type": "bargauge"
    }
  ],
  "refresh": "10s",
  "schemaVersion": 20,
  "style": "dark",
  "tags": [
    "demo"
  ],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "2s",
      "5s",
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ],
    "time_options": [
      "5m",
      "15m",
      "1h",
      "6h",
      "12h",
      "24h",
      "2d",
      "7d",
      "30d"
    ]
  },
  "timezone": "",
  "title": "Bar Gauge",
  "uid": "vmie2cmWz",
  "version": 8
}






