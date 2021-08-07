# Create Server view 


class ServerView: 
    className = "ServerView"

    @classmethod
    def showCrawlMenu(cls):
        print('\n\n')
        print('1. Video Crawling')
        print('2. Video content')
        print('3. Download Video ')
        print('4. Search Video')
        print('5. Exit')

        
    @classmethod 
    def selectMenuNum():
        return int(input("select Menu >> "))
