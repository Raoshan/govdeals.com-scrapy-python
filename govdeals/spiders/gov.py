import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&kWord={}&whichForm=vehicle&searchPg=Main'

class GovSpider(scrapy.Spider):
    name = 'gov'

    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):
        for item in response.xpath('//*[@id="boxx_row"]'):
            link = "https://www.govdeals.com/"+item.xpath("//div[@id='result_col_2']/a/@href").get()
            # print(link)
            name = item.xpath("//div[@id='result_col_2']/a/text()").get()
            # print(name)
            image = "https://www.govdeals.com"+item.xpath('//*[@id="result_col_1"]/a/img/@src').get()
            # print(image)
            auction_date = item.xpath('//*[@id="result_col_4"]/label/text()').get()
            # print(auction_date)
            lot_id = item.css('div.small::text').get()
            # print(lot_id)
            loc = item.xpath("//div[@class='col-10 col-sm-10 col-md-10 col-lg-2 col-xl-2']").get().strip()            
            loc = loc[:-19]
            location = loc[-18:].strip()            
            print(location)

            yield{            
            'product_url' : link,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : locals,           
            'product_name' : name,            
            'lot_id' : lot_id,          
            'auctioner' : "",
            'website' : "govdeals"            
            }


   
            
        href = response.xpath('//div[@id="pagination_1"]/ul/li[last()-1]/a/@href').get()        
        if href is not None:
            link = "https://www.govdeals.com/"+href            
            yield scrapy.Request(link,callback=self.parse,cb_kwargs={'index':index})
        
   
        