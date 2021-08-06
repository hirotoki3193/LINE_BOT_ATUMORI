{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "6d0194ef",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: flask in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (1.1.2)\n",
      "Requirement already satisfied: click>=5.1 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from flask) (7.1.2)\n",
      "Requirement already satisfied: itsdangerous>=0.24 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from flask) (1.1.0)\n",
      "Requirement already satisfied: Werkzeug>=0.15 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from flask) (1.0.1)\n",
      "Requirement already satisfied: Jinja2>=2.10.1 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from flask) (2.11.3)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from Jinja2>=2.10.1->flask) (1.1.1)\n"
     ]
    }
   ],
   "source": [
    "!pip3 install flask\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "8b3c652f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting line-bot-sdk\n",
      "  Downloading line_bot_sdk-1.19.0-py2.py3-none-any.whl (68 kB)\n",
      "Requirement already satisfied: requests>=2.0 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from line-bot-sdk) (2.25.1)\n",
      "Requirement already satisfied: future in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from line-bot-sdk) (0.18.2)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (2020.12.5)\n",
      "Requirement already satisfied: idna<3,>=2.5 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (2.10)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (1.26.4)\n",
      "Requirement already satisfied: chardet<5,>=3.0.2 in e:\\users\\levelcoa\\anaconda3\\lib\\site-packages (from requests>=2.0->line-bot-sdk) (4.0.0)\n",
      "Installing collected packages: line-bot-sdk\n",
      "Successfully installed line-bot-sdk-1.19.0\n"
     ]
    }
   ],
   "source": [
    "!pip3 install line-bot-sdk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "5e12b979",
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, request, abort\n",
    "import os\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "cbf64d7e",
   "metadata": {},
   "outputs": [],
   "source": [
    "from linebot import(LineBotApi,WebhookHandler)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "25ab0dd3",
   "metadata": {},
   "outputs": [],
   "source": [
    "from linebot.exceptions import (\n",
    "    InvalidSignatureError\n",
    ")\n",
    "from linebot.models import (\n",
    "    MessageEvent, TextMessage, TextSendMessage,\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "94f6382e",
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)\n",
    "\n",
    "#環境変数取得\n",
    "YOUR_CHANNEL_ACCESS_TOKEN = os.environ['LINE_BOT_ACCESS_TOKEN']\n",
    "YOUR_CHANNEL_SECRET = os.environ[\"LINE_BOT_SECRET\"]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "156de04d",
   "metadata": {},
   "outputs": [],
   "source": [
    "line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)\n",
    "handler = WebhookHandler(YOUR_CHANNEL_SECRET)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "fea80b49",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def hello_world():\n",
    "    return \"hello world!\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "c6f273af",
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/callback\", methods=['POST'])\n",
    "def callback():\n",
    "    # get X-Line-Signature header value\n",
    "    signature = request.headers['X-Line-Signature']\n",
    "\n",
    "    # get request body as text\n",
    "    body = request.get_data(as_text=True)\n",
    "    app.logger.info(\"Request body: \" + body)\n",
    "\n",
    "    # handle webhook body\n",
    "    try:\n",
    "        handler.handle(body, signature)\n",
    "    except InvalidSignatureError:\n",
    "        abort(400)\n",
    "\n",
    "    return 'OK'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "5f01b7ec",
   "metadata": {},
   "outputs": [],
   "source": [
    "@handler.add(MessageEvent, message=TextMessage)\n",
    "def handle_message(event):\n",
    "    line_bot_api.reply_message(\n",
    "        event.reply_token,\n",
    "        TextSendMessage(text=event.message.text))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c76e7318",
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "int() argument must be a string, a bytes-like object or a number, not 'NoneType'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-9-f2a9724c6cd5>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[1;32mif\u001b[0m \u001b[0m__name__\u001b[0m \u001b[1;33m==\u001b[0m \u001b[1;34m\"__main__\"\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[1;31m#    app.run()\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 3\u001b[1;33m     \u001b[0mport\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mint\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mos\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mgetenv\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m\"PORT\"\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      4\u001b[0m     \u001b[0mapp\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mrun\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mhost\u001b[0m\u001b[1;33m=\u001b[0m\u001b[1;34m\"0.0.0.0\"\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mport\u001b[0m\u001b[1;33m=\u001b[0m\u001b[0mport\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mTypeError\u001b[0m: int() argument must be a string, a bytes-like object or a number, not 'NoneType'"
     ]
    }
   ],
   "source": [
    "if __name__ == \"__main__\":\n",
    "#    app.run()\n",
    "    port = int(os.getenv(\"PORT\"))\n",
    "    app.run(host=\"0.0.0.0\", port=port)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0f1aac14",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
