import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'


def parse_notice(link, today):
    try:
        print(f'Getting information from {link}')
        response_notice = requests.get(link)

        if response_notice.status_code == 200:
            notice = response_notice.content.decode('utf-8')
            notice_parsed = html.fromstring(notice)

            try:
                title = notice_parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                author = notice_parsed.xpath(XPATH_AUTHOR)[0]
                summary = notice_parsed.xpath(XPATH_SUMMARY)[0]
                body = notice_parsed.xpath(XPATH_BODY)
                print('All information was extracted correctly')

            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                print(f'Saving information in {today}/{title}.txt')

                f.write(title)
                f.write('\n\n')
                f.write(author)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response_notice.status_code}')

    except ValueError as ve:
        print(ve)

    except Exception as e:
        print(e)


def parse_home():
    try:
        print(f'Getting information from {HOME_URL}')
        response = requests.get(HOME_URL)

        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(f'{len(links_to_notices)} notices were found')
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            
            if not os.path.isdir(today):
                print(f'Creating folder {today}')
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)

    except Exception as e:
        print(e)


def run():
    parse_home()


if __name__ == '__main__':
    run()