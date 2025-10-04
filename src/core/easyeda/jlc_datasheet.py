import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


class JLCDatasheet:
    def __init__(self, export_path=None):
        """
        初始化JLC数据表下载器
        
        Args:
            export_path: 导出路径，数据手册将保存在该路径的datasheet子目录中
        """
        # 设置更完整的请求头，模拟真实浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.szlcsc.com/',
            'Priority': 'u=0, i'
        }
        
        # 设置导出路径
        self.export_path = export_path
        
        # 创建保存PDF的目录
        if export_path:
            self.pdf_dir = Path(export_path) / "datasheet"
        else:
            self.pdf_dir = Path("datasheet")
            
        # 确保目录存在
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

    def search_product(self, keyword):
        """
        搜索元器件
        :param keyword: 搜索关键词(元器件编号ID)
        :return: 网页内容
        """
        try:
            # 构造URL
            url = f"https://so.szlcsc.com/global.html?k={keyword}"
            
            # 发送GET请求
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 返回网页内容
            return response.text
        except requests.RequestException as e:
            print(f"搜索产品时出错: {e}")
            return None

    def extract_product_url(self, html_content):
        """
        从搜索结果中提取第一个产品的购买链接
        :param html_content: 搜索结果页面HTML内容
        :return: 第一个产品的购买链接
        """
        if not html_content:
            return None
        
        try:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 优先查找具有data-spm="n"属性的a标签，这是产品链接的标识
            target_element = soup.find('a', {'data-spm': 'n'})
            
            # 如果没找到，尝试其他方法
            if not target_element:
                # 查找具有data-spm属性的任意a标签
                target_element = soup.find('a', {'data-spm': True})
            
            # 如果仍然没找到，使用XPath路径查找
            if not target_element:
                target_element = soup.select_one('#__next main div div div div div:nth-child(6) div:nth-child(2) div section div div div div:nth-child(2) dl dd a')
            
            # 如果仍然没找到，尝试更宽松的选择器
            if not target_element:
                target_element = soup.select_one('#__next section div dl dd a')
            
            # 最后的备选方案：查找页面中第一个dl dd a结构
            if not target_element:
                dl_elements = soup.find_all('dl')
                for dl in dl_elements:
                    dd = dl.find('dd')
                    if dd:
                        a_tag = dd.find('a')
                        if a_tag and a_tag.get('href'):
                            target_element = a_tag
                            break
            
            # 如果找到了目标元素，提取href属性
            if target_element:
                href = target_element.get('href')
                if href:
                    # 只保留问号之前的部分作为完整的产品链接
                    if '?' in href:
                        href = href.split('?')[0]
                        print(f"找到第一个产品的购买链接: {href}")
                    # 如果是相对路径，转换为绝对路径
                    if href.startswith('//'):
                        href = 'https:' + href
                    elif href.startswith('/'):
                        href = 'https://item.szlcsc.com' + href
                    elif not href.startswith('http'):
                        # 处理其他相对路径情况
                        href = 'https://item.szlcsc.com' + href
                    return href
            
            print("未找到产品链接")
            return None
        except Exception as e:
            print(f"解析产品链接时出错: {e}")
            return None

    def fetch_product_page(self, url):
        """
        获取产品页面内容
        :param url: 产品页面URL
        :return: 网页内容
        """
        try:
            # 发送GET请求
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 返回网页内容
            return response.text
        except requests.RequestException as e:
            print(f"获取产品页面内容时出错: {e}")
            return None

    def extract_pdf_link(self, html_content):
        """
        从产品页面HTML中提取PDF下载链接
        :param html_content: 产品页面HTML内容
        :return: PDF下载链接
        """
        if not html_content:
            return None
        
        try:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 方法1: 查找id为"item-pdf-down"的元素（保持向后兼容）
            pdf_link_element = soup.find(id="item-pdf-down")
            
            if pdf_link_element:
                # 提取href属性
                pdf_href = pdf_link_element.get('href')
                if pdf_href:
                    # 如果是相对路径，需要转换为绝对路径
                    if pdf_href.startswith('//'):
                        pdf_href = 'https:' + pdf_href
                    elif pdf_href.startswith('/'):
                        pdf_href = 'https://item.szlcsc.com' + pdf_href
                    
                    # 只保留问号之前的部分
                    if '?' in pdf_href:
                        pdf_href = pdf_href.split('?')[0]
                    
                    return pdf_href
            
            # 方法2: 查找包含PDF下载链接的script标签
            # 查找所有script标签
            scripts = soup.find_all('script')
            
            # 在script标签中查找PDF链接
            for script in scripts:
                if script.string:
                    # 查找包含pdfUrl或PDF链接的JavaScript代码
                    import re
                    pdf_match = re.search(r'pdfUrl["\']?\s*[:=]\s*["\']([^"\']+)"\']', script.string, re.IGNORECASE)
                    if pdf_match:
                        pdf_href = pdf_match.group(1)
                        # 如果是相对路径，需要转换为绝对路径
                        if pdf_href.startswith('//'):
                            pdf_href = 'https:' + pdf_href
                        elif pdf_href.startswith('/'):
                            pdf_href = 'https://item.szlcsc.com' + pdf_href
                        
                        # 只保留问号之前的部分
                        if '?' in pdf_href:
                            pdf_href = pdf_href.split('?')[0]
                        
                        return pdf_href
            
            # 方法3: 查找页面中其他可能的PDF链接
            # 查找所有a标签，寻找包含.pdf的链接
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if '.pdf' in href.lower():
                    # 如果是相对路径，需要转换为绝对路径
                    if href.startswith('//'):
                        href = 'https:' + href
                    elif href.startswith('/'):
                        href = 'https://item.szlcsc.com' + href
                    elif not href.startswith('http'):
                        # 处理相对路径
                        continue
                    
                    # 只保留问号之前的部分
                    if '?' in href:
                        href = href.split('?')[0]
                    return href
            
            print("未找到PDF下载链接")
            return None
        except Exception as e:
            print(f"解析PDF下载链接时出错: {e}")
            return None

    def download_pdf(self, url, filename):
        """
        下载PDF文件
        :param url: PDF文件URL
        :param filename: 保存的文件名
        :return: 是否成功下载
        """
        try:
            # 完整的文件路径
            filepath = self.pdf_dir / filename
            
            # 下载文件
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"PDF文件已成功下载到: {filepath}")
            return True
        except Exception as e:
            print(f"下载PDF文件时出错: {e}")
            return False

    def download_datasheet(self, keyword, filename=None):
        """
        下载元器件数据表的完整流程
        :param keyword: 元器件编号
        :param filename: 保存的文件名（可选）
        :return: 是否成功下载
        """
        print(f"正在搜索元器件数据手册: {keyword}")
        
        # 1. 搜索产品
        search_result = self.search_product(keyword)
        if not search_result:
            print("搜索产品失败")
            return False
        
        print("成功获取搜索结果，正在提取产品链接:")
        
        # 2. 提取产品链接
        product_url = self.extract_product_url(search_result)
        if not product_url:
            print("提取产品链接失败")
            return False
        
        print(f"成功提取到产品链接: {product_url}")
        
        # 3. 获取产品页面
        product_page = self.fetch_product_page(product_url)
        if not product_page:
            print("获取产品页面失败")
            return False
        
        print("成功获取产品页面，正在提取PDF链接:")
        
        # 4. 提取PDF链接
        pdf_url = self.extract_pdf_link(product_page)
        if not pdf_url:
            print("提取PDF链接失败")
            return False
        
        print(f"成功提取到PDF链接: {pdf_url}")
        
        # 5. 下载PDF
        if not filename:
            filename = f"{keyword}.pdf"
        
        print(f"正在下载PDF文件并保存为: {filename}")
        success = self.download_pdf(pdf_url, filename)
        
        if success:
            print(f"数据手册 {filename} 下载成功")
        else:
            print(f"数据手册 {filename} 下载失败")
            
        return success

