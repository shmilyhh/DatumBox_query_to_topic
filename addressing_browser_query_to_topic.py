import os
import json
import sys
import getopt
from DatumBox import DatumBox

def get_topic_category(api_key, text):
	datum_box = DatumBox(api_key)
	return datum_box.topic_classification(text)

def main(argv):
	api_key = ''
	in_filename = ''
	out_filename = ''
	index = 0
	try:
		opts, args = getopt.getopt(argv, "h:k:i:o:d:", ["api_key=", "in_filename=", "out_filename", "index"])
	except:
		print "addressing_browser_query_to_topic.py -h <api key> -i <filename> -o <filename>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print "addressing_browser_query_to_topic.py -h <api key> -i <filename> -o <filename>"
			sys.exit()
		elif opt == "-k":
			api_key = arg
			print api_key
		elif opt == "-i":
			in_filename = arg
			print in_filename
		elif opt == "-o":
			out_filename = arg
			print out_filename
		elif opt == "-d":
			index = arg
			print index

	data_path = "./unique_search_queries"
	result_path = "./result"
	with open(os.path.join(data_path, in_filename)) as fp:
		data = json.load(fp)
	topics = {}
	i = 0
	for d in data:
		print i
		if i <= int(index):
			i += 1
			continue
				
		try:
			topic = get_topic_category(api_key, d)
		except:
			print
			print "==============================="
			print d
			print i
			print "==============================="
			with open(os.path.join(result_path, out_filename), "w") as fp:
				json.dump(topics, fp, indent=4)
			sys.exit()

		if topic not in topics:
			topics[topic] = [d]
		else:
			topics[topic].append(d)
		i += 1
	with open(os.path.join(result_path, out_filename), "w") as fp:
		json.dump(topics, fp, indent=4)

if __name__ == '__main__':
	main(sys.argv[1:])