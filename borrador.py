from __main__ import app

import sys
import csv
from selenium import webdriver
import time
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        
from flask import Flask , render_template, url_for, redirect
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/tripadvisor', methods=['GET', 'POST'])
def tripadvisor():
    return render_template('tripadvisor.html')


@app.route('/tripadvisorweb', methods=['GET', 'POST'])
@login_required

def tripadvisorweb():

    filt=4 
    num_page=1

 # default tripadvisor website of restaurant
    url = "https://www.tripadvisor.es/Restaurants-g187497-Barcelona_Catalonia.html"

    # if you pass the inputs in the command line
    path = '/Users/alvarodelamaza/Reservas Upna/env/bin/chromedriver 2'

    # Import the webdriver
    driver = webdriver.Chrome(path)
    driver.get(url)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    # Accept cookies
    time.sleep(3)
    cookies=driver.find_element_by_xpath(".//button[@id='_evidon-accept-button']")
    driver.execute_script("arguments[0].click();", cookies)
    time.sleep(3)

    
      
    

    Buscar=driver.find_element_by_xpath(".//input[@class='_3qLQ-U8m']")
    Buscar.send_keys('Restaurante Ecologico')
    Buscar.send_keys(Keys.ENTER)
    time.sleep(1)
        
        
        
    
        
        
    restaurantssss=[]
    prices=[]
    baresT=[]
    prixT=[]
    mailsT=[]
    emailsT=[]
    direccionT=[]
    total=[]
    k=0
    if filt==3:
            
            #masmas=driver.find_elements_by_xpath("//*[@id='BODY_BLOCK_JQUERY_REFLOW']/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[3]/div/div/span[2]")
            #driver.execute_script("arguments[0].click();", masmas)
            #masmas[0].click
            #time.sleep(2)
            
            barico=driver.find_elements_by_xpath("//*[@id='search-filters']/ul/li[4]/a")
            driver.execute_script("arguments[0].click();", barico)
            #barico[0].click()
            
            time.sleep(2)
    while k< num_page:
        if filt==4:
            
            restaurantss=driver.find_elements_by_xpath(".//div[@class='result-title']")
        
        else:
            restaurantss= driver.find_elements_by_xpath(".//a[@class='_15_ydu6b']")
        k=k+1
        
        item=[]
        for l in range(len(restaurantss)):
            item.append('a')
        for i in range(len(restaurantss)):
            
            clicar=restaurantss[i]
            window_before = driver.window_handles[0]
            driver.execute_script("arguments[0].click();", clicar)
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            time.sleep(1)
            
            email=(driver.find_elements_by_xpath('.//div[@class="_36TL14Jn _3jdfbxG0"]'))
            
                
            try:    
                name=(driver.find_element_by_xpath('.//h1[@class="_3a1XQ88S"]')).text
            except NoSuchElementException:
                name='-'
            try:
                direccion=(driver.find_element_by_xpath('.//span[@class="_2saB_OSe"]')).text
            except NoSuchElementException:
                direccion='-'
            try:
                telefono=(driver.find_element_by_xpath('.//span[@class="_15QfMZ2L"]'))
                telefono=telefono.find_element_by_tag_name('a').text
            except NoSuchElementException:
                telefono='-'
            try:
                barrio=(driver.find_element_by_xpath('.//span[@class="_2saB_OSe _1OBMr94N"]')).text
            except NoSuchElementException:
                barrio='-'
            try:
                precio=(driver.find_elements_by_xpath('.//div[@class="_1XLfiSsv"]'))
                mix=[prc.text for prc in precio]
            except NoSuchElementException:
                precio='-'
            #try:
            # cocina=(driver.find_element_by_xpath('.//div[@class="_3UjHBXYa"]'))
                #cocina=cocina.find_element_by_xpath('.//div[@class="_1XLfiSsv"]').text
            #except NoSuchElementException:
            # cocina=['-']
            datos=['-','-']
            for m in range(len(email)):
                try:
                    emaill=email[m].find_element_by_tag_name('span') 
                except:
                    datos[m]='-'
                    break
                try:
                    emailll=emaill.find_element_by_tag_name('a')
                except NoSuchElementException:
                    datos[m]='-'
                    break
                try:
                    mailss =emailll.get_attribute('href')
                    print(mailss)
                    datos[m]=mailss
                except NoSuchElementException:
                    datos[m]='-'
                    break
            datos[1]=datos[1][:-10]    
            item=[]
            item.append(name)
            item.append(direccion)
            item.append(datos[0])
            
            item.append((datos[1]))
            item.append(telefono)
            item.append(barrio)
            if len(mix)>0:
                item.append(mix[0])
            if len(mix)>1:
                item.append(mix[1])
            if len(mix)>2:
                item.append(mix[2]) 
            total.append(item)
            
            time.sleep(1)
            driver.close()
            driver.switch_to.window(window_before)
        if filt==4:
            time.sleep(1)    
            next_pagee=driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]')
            driver.execute_script("arguments[0].click();", next_pagee)
            time.sleep(2)
        else:
            time.sleep(1)    
            next_page=driver.find_element_by_xpath('.//a[@class="nav next rndBtn ui_button primary taLnk"]')
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(2)


    driver.quit()  

    restaa = pd.DataFrame(total, 
                    columns=['Restaurants','Adress', 'Web', 'Email', 'Phone', 'Area','Price','Style','Diets' ])
    headers = ('Restaurants','Adress', 'Web', 'Email', 'Phone', 'Area','Price','Style','Diets' ) 
    data = total
    return render_template('tripadvisorweb.html', data=data, headers=headers)

    
