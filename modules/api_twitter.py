import urllib
import io
from requests_oauthlib import OAuth1
import requests
import sys

def main(word):

    # APIの秘密鍵
    CK = 'JsyR1Yt5mdXewsLBry42kwaQl' # コンシューマーキー
    CKS = 'nTZ8ALJ0wlfhxAPBTEdfB9nZSqpd3JKFe1VyMLuYc0PJuiw9kJ' # コンシューマーシークレット
    AT = '1169459456196804608-fUvNRBXnRmkx0wzMrWoWCoo14ZqUK1' # アクセストークン
    ATS = '2mweQTDTW1Egw81A7x6bRwP2aX9bbzEbDz95BzZH98DXZ' # アクセストークンシークレット
    count = 100 # 一回あたりの検索数(最大100/デフォルトは15)
    range = 5 # 検索回数の上限値(最大180/15分でリセット)
    # インスタンス生成
    get = Get_tweets()
    # ツイート検索・テキストの抽出
    tweets = get.search_tweets(CK, CKS, AT, ATS, word, count, range)
    return tweets
    print("")

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
