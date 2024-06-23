from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import traceback
import time
import json





service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)







def choose_filter(nfilter, index):

	
	print('choose_filter', nfilter, index)
	filter = filters[nfilter]

	
	
	



	
	for t2 in range(10):
		estatus = ''
		try:
			
			
			for u1 in range(10):
				time.sleep(0.5)
				if 'ant-select-selection__clear' not in filter.get_attribute('innerHTML'): break

				clear = filter.find_element(By.CSS_SELECTOR, "span[class='ant-select-selection__clear']")
				for u in range(2):
					try:
						clear.click()
						
						time.sleep(0.2)
						break
					except:
						try:
							homed = driver.find_element(By.CSS_SELECTOR, "div[class='home-vue']")
							driver.execute_script("arguments[0].scrollIntoView(true);", homed)
							time.sleep(0.5)
						except:
							pass

			filter.click()

		except:
			traceback.print_exc()
			
		

		for t in range(10):
			time.sleep(0.5)

			try:
				dropdowns = driver.find_elements(By.CSS_SELECTOR, 
					"ul[class='ant-select-dropdown-menu ant-select-dropdown-menu-vertical ant-select-dropdown-menu-root")

				#print(len(dropdowns), 'dropdowns')

				dropdown = dropdowns[nfilter]

				lis = dropdown.find_elements(By.CSS_SELECTOR, 'li')

				print('filter', nfilter, 'has', len(lis), 'items')

				if not lis: raise RuntimeError('dropdown is empty')

				empty = 0
				num = 0
				for itm in lis:
					if not itm.text.strip():
						empty += 1
						continue
						
					
					if 'ant-empty-image' in itm.get_attribute('innerHTML'):
						estatus = 'empty_image'
						raise RuntimeError('confirmed empty')
						
					
					print(itm.text)

					if num == index:
						itm.click()
						time.sleep(0.5)

						if index >= len(lis)-1:
							print('end of dropdown reached')
							return 0
						else:
							return 1
					
					num += 1
				
				if empty == len(lis):
					estatus = 'empty_text'
					raise RuntimeError('dropdown empty text')
					
			except:
				traceback.print_exc()

	if estatus == 'empty_text' or estatus == 'empty_image': return -1
	raise RuntimeError('max tries reached')
	

		


def do_select_glass():
	for t in range(5):
		try:
			time.sleep(0.2)
			glasses = filters[4].find_element(By.CSS_SELECTOR, "div[class='glasses']").find_elements(By.CSS_SELECTOR, 'div')

			eglasses = []
			for glass in glasses:
				cls = glass.get_attribute('class')
				print(cls)
				if 'disabled' in cls: continue
				eglasses.append(glass)
			
			if not eglasses:
				raise RuntimeError('all glasses disabled')

			break
		except:
			traceback.print_exc()
	else:
		raise RuntimeError('max tries reached')
	
	for glass in eglasses:
		try:
			glass.click()
		except:
			traceback.print_exc()

	choose_glass()



def choose_glass():
	for t in range(5):
		try:
			time.sleep(0.2)
			products = driver.find_element(By.CSS_SELECTOR, "div[class='products__mobile']").find_elements(By.CSS_SELECTOR, "div[class='product__details']")
			if not products:
				raise RuntimeError('empty products')
			
			for product in products:
				do_product(product)
			
			return
		except:
			traceback.print_exc()

	raise RuntimeError('max tries reached')
	
	



def load_price(product):
	for t in range(5):
		try:
			product.find_element(By.CSS_SELECTOR, "button[class='btn btn-price']").click()
		except:
			traceback.print_exc()

		for t in range(5):
		
			time.sleep(0.5)
			
			try:
				price = product.find_element(By.CSS_SELECTOR, "div[class='price-total']").text
				if not price.strip():
					raise RuntimeError('empty price')
				
				print(price)
				return price
			except:
				traceback.print_exc()
	
	raise RuntimeError('max tries reached')


def do_modal(modal):
	print(modal.get_attribute('innerHTML'))
	items = modal.find_elements(By.CSS_SELECTOR, "li[class='list-item']")

	res = {}
	for item in items:
		name = item.find_element(By.CSS_SELECTOR, "div[class='list-item__name']").text
		value = item.find_element(By.CSS_SELECTOR, "div[class='list-item__value']").text
		print(name, value)
		res[name] = value

	modal.find_element(By.CSS_SELECTOR, "button[class='btn modal__close']").click()

	time.sleep(0.5)

	return res


def open_info(product):
	for t in range(5):
		try:
			product.find_element(By.CSS_SELECTOR, "button[class='product__info']").click()
		except:
			traceback.print_exc()
		
		time.sleep(0.5)
		
		try:
			modal = driver.find_element(By.CSS_SELECTOR, "div[class='info-modal info-modal--order info-modal--active")
			if not modal:
				raise RuntimeError('no modal')
			
			return do_modal(modal)
		except:
			traceback.print_exc()


		return
		
	raise RuntimeError('max tries reached')

def do_product(product):
	print (product)
	print(product.get_attribute('innerHTML'))
	title = product.find_element(By.CSS_SELECTOR, "div[class='product__title']").text
	print(title)

	status = product.find_element(By.CSS_SELECTOR, "div[class='status-box']").find_element(By.CSS_SELECTOR, "div").text
	print(status)

	

	res = open_info(product)
	price = load_price(product)
	res['ecode'] = title
	res['price'] = price
	res['status'] = status

	outfile = open('out.json', 'a')
	outfile.write(json.dumps(res)+'\n')
	outfile.close()


	


	
		

marka = 0
model = 0
god = 0
kuzov = 0

try:
	pos = json.load(open('pos.json'))
	marka, model, god, kuzov = pos
	print('resume', marka, model, god, kuzov)
except:
	print('new start')

all_done = False

while True:
	try:
		driver.get("https://autoglass.net.ua/")

		homed = driver.find_element(By.CSS_SELECTOR, "div[class='home-vue']")
		driver.execute_script("arguments[0].scrollIntoView(true);", homed)
		time.sleep(0.5)

		while True:
			filters = driver.find_elements(By.CSS_SELECTOR, "div[class='filter__item']")
			if len(filters) >= 5: break
			print('no dropdowns on main page')
			time.sleep(0.5)

	
		while True:
			n0 = choose_filter(0, marka)

			while True:
				n1 = choose_filter(1, model)

				while n1 >= 0:
					n2 = choose_filter(2, god)
					
					while n2 >= 0:
						n3 = choose_filter(3, kuzov)
						json.dump([marka, model, god, kuzov], open('pos.json', 'w'))
						if n3 >= 0:
							do_select_glass()
						
						if n3 > 0:
							kuzov += 1
						else:
							print('next god')
							kuzov = 0
							break
					if n2 > 0:
						god += 1
					else:
						print('next model')
						god = 0
						break
					
				if n1 > 0:
					model += 1
				else:
					print('next marka')
					model = 0
					break
				
			if n0 > 0:
				marka += 1
			else:
				print('finished')
				all_done = True
				break
	except:
		traceback.print_exc()
		time.sleep(10)
	
	if all_done:
		break






	


