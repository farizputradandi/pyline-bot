from googletrans import Translator 
translator = Translator()
tsrc= "en"
tdst="id" 
tword="chicken wings"
# print(translator.translate(tword, src=tsrc, dest=tdst)) 
print(translator.translate("nama saya fariz, saya lahir disurabaya", src="id", dest="en").text) 

# translations = translator.translate(['nama saya farizz', 'saya lahir disurabaya', 'surabaya adalah ibukota surabaya'],src='id', dest='en')
# for translation in translations:
# 	print(translation.origin, ' -> ', translation.text)
# 	  
# print(translator.translate(tword, src=tsrc, dest=tdst).text) 