import urllib
import io
from requests_oauthlib import OAuth1
import requests
import sys

def main(word):

    # APIの秘密鍵
    CK = '2aLzCMZtkdqDsRhKYc4ilARFT' # コンシューマーキー
    CKS = 'zbMrEdVndKVcu1kx1X9YhptR0QW2TOvB9VBXgWoOJOJKKjSisF' # コンシューマーシークレット
    AT = '929970261897633792-T9SwwxvHclI4h9WLcaFd0RzE9kSmqWn' # アクセストークン
    ATS = 'EOOOPKc1bzl69ieXfP9cUJB76KJDbo4vdePsjAFgreKBS' # アクセストークンシークレット
    count = 100 # 一回あたりの検索数(最大100/デフォルトは15)
    range = 5 # 検索回数の上限値(最大180/15分でリセット)
    # インスタンス生成
    get = Get_tweets()
    # ツイート検索・テキストの抽出
    tweets = get.search_tweets(CK, CKS, AT, ATS, word, count, range)
    return tweets

class Get_tweets:

    def search_tweets(self, CK, CKS, AT, ATS, word, count, range):
        # 文字列設定
        word2 = word;
        word += ' exclude:retweets' # RTは除く
        word = urllib.parse.quote_plus(word)
        # リクエスト
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)
        auth = OAuth1(CK, CKS, AT, ATS)

        response = requests.get(url, auth=auth)

        data = response.json()

        statuses = data.get("statuses")

        if statuses is None: 
            return response
        data = data['statuses']

        resultData = []
        for d in data:
            #resultData.append(format(d["text"]))
            resultData.append(d)

        return resultData

        # 2回目以降のリクエスト
        cnt = 0
        tweets = []
        while True:
            if len(data) == 0:
                break
            cnt += 1
            if cnt > range:
                break
            for tweet in data:
                tweets.append(tweet['text'])
                maxid = int(tweet["id"]) - 1
            url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+word+"&count="+str(count)+"&max_id="+str(maxid)
            response = requests.get(url, auth=auth)
            try:
                data = response.json()['statuses']
            except KeyError: # リクエスト回数が上限に達した場合のデータのエラー処理
                print('上限まで検索しました')
                break
        return tweets

if __name__ == '__main__':
    main()
