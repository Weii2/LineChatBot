main_menu = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/KhzZ5X2.png",
        "offsetTop": "sm"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "介紹",
              "text": "功能介紹"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg",
        "margin": "none"
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/0oFnAwh.png",
        "offsetTop": "sm"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "記帳",
              "text": "記帳"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg"
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/rbiq4ML.png"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "查看收支圖表",
              "text": "查看收支圖表"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg"
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/lC65COo.png"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "本月目前結餘",
              "text": "本月目前結餘"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg"
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/y008y53.gif",
        "offsetTop": "sm"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "觀看影片",
              "text": "觀看影片"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg"
      }
    },
    {
      "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/1P0GA9A.png",
        "offsetTop": "sm"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "查看fsm diagram",
              "text": "查看fsm diagram"
            },
            "color": "#ffffff",
            "offsetBottom": "sm"
          },
          {
            "type": "spacer",
            "size": "xs"
          }
        ],
        "backgroundColor": "#ff9900",
        "offsetTop": "lg",
        "margin": "none"
      }
    }
  ]
}

se_type = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/vtdoz18.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "fit",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "margin": "none",
    "offsetTop": "none"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請選擇記帳類型",
        "align": "center",
        "color": "#73BF00"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "支出",
          "text": "支出"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "收入",
          "text": "收入"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "查看所有紀錄",
          "text": "查看所有紀錄"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}

enter_success = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "text"
      },
      {
        "type": "text",
        "text": "text"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "編輯",
          "text": "編輯"
        },
        "margin": "xl",
        "height": "sm",
        "style": "secondary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "主選單"
        },
        "margin": "md",
        "height": "sm",
        "style": "primary"
      }
    ]
  }
}

edit_success = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "已完成編輯"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "主選單"
        },
        "height": "sm",
        "style": "primary",
        "margin": "lg"
      }
    ]
  }
}

shiba_bar = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "image",
        "url": "https://i.imgur.com/rB9b5S4.png",
        "size": "full"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "支出",
            "align": "start"
          },
          {
            "type": "text",
            "text": "目前結餘",
            "align": "center"
          },
          {
            "type": "text",
            "text": "收入",
            "align": "end"
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "spend",
            "align": "start"
          },
          {
            "type": "text",
            "text": "spea",
            "align": "center"
          },
          {
            "type": "text",
            "text": "earn",
            "align": "end"
          }
        ]
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "主選單"
        }
      }
    ]
  }
}

yt_video = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "text",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀看影片",
              "uri": "http://linecorp.com/"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "text",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀看影片",
              "uri": "http://linecorp.com/"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "text",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀看影片",
              "uri": "http://linecorp.com/"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "text",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀看影片",
              "uri": "http://linecorp.com/"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "text",
            "align": "center"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "觀看影片",
              "uri": "http://linecorp.com/"
            }
          }
        ]
      }
    }
  ]
}

intro = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "功能介紹",
        "size": "lg",
        "weight": "bold",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": "記帳 – 記錄每筆支出及收入",
            "offsetStart": "lg"
          }
        ],
        "borderWidth": "semi-bold"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": "查看收支圖表",
            "offsetStart": "lg"
          }
        ],
        "borderWidth": "semi-bold"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": "計算目前結餘",
            "offsetStart": "lg"
          }
        ],
        "borderWidth": "semi-bold"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
          },
          {
            "type": "text",
            "text": "觀看可愛狗狗影片降低花錢慾望",
            "offsetStart": "lg"
          }
        ],
        "borderWidth": "semi-bold"
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "使用說明",
            "size": "lg",
            "weight": "bold",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://i.imgur.com/1UamX1Q.png"
              },
              {
                "type": "text",
                "text": "輸入主選單來進行操作",
                "offsetStart": "lg"
              }
            ],
            "borderWidth": "semi-bold"
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://i.imgur.com/1UamX1Q.png"
              },
              {
                "type": "text",
                "text": "依照按鈕與指示來執行各項功能",
                "offsetStart": "lg"
              }
            ],
            "borderWidth": "semi-bold"
          },
          {
            "type": "separator"
          }
        ],
        "offsetTop": "lg"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "返回主選單",
          "text": "主選單"
        }
      }
    ]
  }
}