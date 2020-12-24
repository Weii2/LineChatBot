# LINE CharBot -- Track your Income & Expenses

Project for TOC 2020

A Line bot based on a finite state machine

## 前言
### 創作動機

對於還沒邁向財富自由的大學生來說，好好管控每天的花費是必要的工作，了解金錢的流向才不會在月底時只能吃泡麵度過

### 目標

傳統手作雖然也是很實際的記帳方式，但相對的也需要花費較多的時間，因此此Project的目標就是製作出便利、容易操作、互動性高的記帳行聊天機器人，使用者只要依據指示就能輕鬆記帳，並透過視覺化圖表分析自己的金錢流向。

## 開發環境
* Ubuntu 18.04
* Python 3.6.9

## 介紹
### 基本資訊
名稱 : 記帳小幫手
![main_icon](https://i.imgur.com/TisBW9J.png)
![bot_info](https://i.imgur.com/86Kcl7W.png)

## 使用說明
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "go to state1"
		* Reply: "I'm entering state1"

	* Input: "go to state2"
		* Reply: "I'm entering state2"


## Finite State Machine
![fsm](./img/show-fsm.png)

