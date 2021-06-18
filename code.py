import csv;

class MempoolTransaction():
	def __init__(self, txid, fee, weight, parents):
		self.txid = txid
		self.fee = fee
		self.weight = weight
		self.parents = parents.split(';')

def parse_mempool_csv():
	with open('mempool.csv') as f:
		return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

# isValid function checks if all the parents transactions are included before
def is_valid(parents, included):
	c = 0
	if(parents[0] == ''):
		return True
	for i in range(len(parents)):
		if(parents[i] in included):
			c = c + 1
	if(c == len(parents)):
		return True
	else:
		return False

if __name__ == "__main__":

	# Maximum weight given in the README file
	max_weight = 4000000

	# Current Total Weight
	weight = 0

	# Current Transaction Weight
	w = 0

	# Mempool list of class objects of MempoolTransaction
	mempool = parse_mempool_csv()

	# Length of the list mempool
	n = len(mempool)

	# Empty list to store the included Trasaction Ids txid
	included = []

	# List to store the few/weight ratio as the first element and the MempoolTransaction object as the second
	fw = [[(float)(mempool[i].fee) / (float)(mempool[i].weight), mempool[i]] for i in range(1, n)]
	# Sorts the fee/weight ratio list in descending order
	fw = sorted(fw, key = lambda x: x[0], reverse=True)

	while((len(fw)!= 0) and (weight < max_weight)):
		flag = False
		for i in range(len(fw)):
			txid = fw[i][1].txid
			w = int(fw[i][1].weight)
			parents = fw[i][1].parents
			if(is_valid(parents, included) and (w + weight <= max_weight)):
				weight = weight + w
				included.append(txid)
				fw.pop(i)
				flag = True
				break;
		if(not flag):
			break;
	
	# block.txt is the output file
	block = open('block.txt', 'w')

	for i in range(len(included)):
		block.write(included[i])
		block.write("\n")
	
	block.close()