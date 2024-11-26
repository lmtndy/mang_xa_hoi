import facebook
import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

class FacebookCollector:
    def __init__(self, access_token):
        try:
            self.access_token = access_token
            self.graph = facebook.GraphAPI(access_token)
        except Exception as e:
            print(f'Loi khoi tao: {e}')

    def check_token_validity(self):
        try:
            me = self.graph.get_object('me', fields = 'id,name')
            print('Token hop le')
            return True
        except Exception:
            print('Token khong hop le')
            return False
        
    def collect_data(self, limit = 5):
        try:
            fields = (
               'id'
               ',message'
               ',created_time'
               ',comments.limit(100).summary(true)'
               '{created_time,from{id,name},message,reactions}'
               ',reactions.limit(100).summary(true)'
               '{id,type,name}'
               ',shares'
               ',type'
            )  
            
            # lấy sai phân
            posts = self.graph.get_object('me/feed')

            for post in posts.get('data', []):
                print('-----------------------------')
                print(post.get('message'))
                print('-----------------------------')
                        
            return posts 
        except Exception:
            pass

    def json_to_excel(self, data, excel_file=None):
        posts = []
        for post in data.get('data', []):
            post_data = {
                'id': post.get('id', ''),
                'created_time': post.get('created_time', ''),
                'message': post.get('message', '') 
            } 
            posts.append(post_data)

        df = pd.DataFrame(posts)
        
        # chuyển đồi create_time asng định dạng datetime
        df['created_time'] = pd.to_datetime(df['created_time'])

        # format lại thời gian cho dễ đọc
        df['created_time'] = df['created_time'].dt.strftime('%Y-%m-%d')

def main():
    ACCESS_TOKEN = 'EAAVvrMU8dAsBOZBCNdW8qKZB9HFjjMQRAvG01d7499vwGgfq058Eqm5DVW8raOlVe607g63Xqpkl05BrgnIdOCvU4xQfT9OgZAfeVCT7nzXywT23HSUaP7ivGrWhBVIAIZAEXUvJ7AUCZCereuQ3cLCesgr2gsjzpLvqrlChYpbaZCvb2vahezAEkuzEO6GeF5Bn2HMNtfaawkUu4VGZCVZCw6SvIwgkYHGpz4QuMdtLeSPLfq9Wp0mp'
    collector = FacebookCollector(ACCESS_TOKEN)

    if (collector.check_token_validity()):
        data = collector.collect_data(limit=2)
        collector.json_to_excel(data)
        
if __name__ == "__main__":
    main()