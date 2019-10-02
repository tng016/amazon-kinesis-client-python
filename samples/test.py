from TaxiDirectory import TaxiDirectory

if __name__== "__main__":
	message = "hello world"
	f=open("log.txt", "a+")
	f.write("%s\r\n" % message)
	f.close()