
import requests
from bs4 import BeautifulSoup

def extract_design_info(soup):
    headings = []
    details = []
    div_tag = soup.find("div", class_="section e")
    if div_tag:
        heading_1 = div_tag.find("h2", class_="transition animate")
        if heading_1:
            headings.append(heading_1.get_text(strip=True))
        p_tag_1 = div_tag.find('p', class_='transition animate')
        if p_tag_1:
            details.append(p_tag_1.get_text(strip=True))
            
    div_tag = soup.find("div", class_="section b")
    if div_tag:
        heading_2 = div_tag.find("h2")
        if heading_2:
            headings.append(heading_2.get_text(strip=True))
        para = div_tag.find("p")
        if para:
            details.append(para.get_text(strip=True))
    combined_headings = '\n'.join(headings) if headings else "Design headings not found"
    combined_details = '\n'.join(details) if details else "Design details not found"
    return {
        'Headings': combined_headings,
        'Details': combined_details
    }
            
def extract_control_info(soup):
    headings=[]
    details=[]
    highlight_box = soup.find('div', {'class': 'box highlights'})
    if highlight_box:
        first_li = highlight_box.find('li')  
        if first_li:
            following_text = first_li.get_text().strip()
            details.append(following_text)
    
        
    combined_headings = '\n'.join(headings) if headings else "Control headings not found"
    combined_details = '\n'.join(details) if details else "Control details not found"
    return {
        'Headings': combined_headings,
        'Details': combined_details
    }
def extract_security_info(soup):
    headings=[]
    details=[]
    div_tag=soup.find("div",class_="section c")
    if div_tag:
        heading_1 = div_tag.find("h2", class_="transition animate")
        if heading_1:
            headings.append(heading_1.get_text(strip=True))
        p_tag_1 = div_tag.find('p', class_='transition animate')
        if p_tag_1:
            details.append(p_tag_1.get_text(strip=True))
    
    div_tag=soup.find("div",class_="des")
    if div_tag:
        heading_1=div_tag.find("h3")
        if heading_1:
            headings.append(heading_1.get_text(strip=True))
        p_tag1=div_tag.find("p")
        if p_tag1:
            details.append(p_tag1.get_text(strip=True))
            
    combined_headings = '\n'.join(headings) if headings else "Security headings not found"
    combined_details = '\n'.join(details) if details else "Security details not found"
    
    return {
        'Headings': combined_headings,
        'Details': combined_details
    }
def extract_dimensions_info(soup):
    headings=[]
    details=[]
    row1=soup.find_all('tr',id='tr_5317')
    for row in row1:
        th = row.find('th')  
        td = row.find('td')
        if th:
            headings.append(th.get_text(strip=True))
        if td:
            details.append(td.get_text(strip=True))
    
    row2 = soup.find_all('tr',id='tr_1564')
    for row in row2:
        th=row.find('th')
        td=row.find('td')
        if th:
            headings.append(th.get_text(strip=True))
        if td:
            details.append(td.get_text(strip=True))
            
    combined_headings = '\n'.join(headings) if headings else "Dimensions headings not found"
    combined_details = '\n'.join(details) if details else "Dimensions details not found"
    
    return {
        'Headings': combined_headings,
        'Details': combined_details
    }
def extract_scheduling_info(soup):
    headings=[]
    details=[]
    div_tag=soup.find("div",class_="section d")
    if div_tag:
        heading_1=div_tag.find("h2")
        if heading_1:
            headings.append(heading_1.get_text(strip=True))
        para=div_tag.find("p")
        if para:
            details.append(para.get_text(strip=True))
    div_tag=soup.find("div",class_="section g")
    if div_tag:
        div1=div_tag.find("div",class_="text transition animate")
        if div1:
            para=div1.find("p")
            if para:
                details.append(para.get_text(strip=True))
    combined_headings = '\n'.join(headings) if headings else "Scheduling headings not found"
    combined_details = '\n'.join(details) if details else "Scheduling details not found"
    
    return {
        'Headings': combined_headings,
        'Details': combined_details
    }

def scrape_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    data = {
        'remote_control': extract_control_info(soup),
        'scheduling_features': extract_scheduling_info(soup),
        'security_features': extract_security_info(soup),
        'dimensions': extract_dimensions_info(soup),
        'design_features': extract_design_info(soup)
    }
    '''print("Scraped Data:")
    for key, value in data.items():
        print(f"{key}: {value}")'''

    # Formatting the output for better readability
    formatted_data = {
        'Remote Control': {
            'Headings': data['remote_control']['Headings'],
            'Details': data['remote_control']['Details']
        },
        'Scheduling Features': {
            'Headings': data['scheduling_features']['Headings'],
            'Details': data['scheduling_features']['Details']
        },
        'Security Features': {
            'Headings': data['security_features']['Headings'],
            'Details': data['security_features']['Details']
        },
        'Dimensions': {
            'Headings': data['dimensions']['Headings'],
            'Details': data['dimensions']['Details']
        },
        'Design Features': {
            'Headings': data['design_features']['Headings'],
            'Details': data['design_features']['Details']
        }
    }
    
    '''for section, data in formatted_data.items():
        print(f"{section}:")
        print(f"Headings: {data['Headings']}")
        print(f"Details: {data['Details']}")
        print()'''

    return formatted_data
