#!pip install pyserini==0.9.4.0
from pyserini.search import SimpleSearcher
from pyserini import analysis, index
import spacy

def write_out(path_index, path_out, query_operation):
	
	searcher = SimpleSearcher(path_index)
	index_utils = index.IndexReader(path_index)

	f = open(path_out, "a")
	searcher.set_bm25(0.9, 0.4)
	searcher.set_rm3(10, 10, 0.5)
	searcher.set_qld(400)
	for x in range(len(number)):
	  hits = searcher.search(query_operation[x],100)

	  # Print the first 10 hits:
	  for i in range(0, 100):
	    #f = open("/content/anserini/june_remove_num.txt", "a")
	    print(f'{number[x]} {"Q0"} {hits[i].docid:15} {i+1:2} {hits[i].score:.5f} {"JUNE"}')
	    f.write(f'{number[x]} {"Q0"} {hits[i].docid:15} {i+1:2} {hits[i].score:.5f} {"JUNE"}\n')
	f.close()  

#Writing all query operations files
write_out("/path/to/index","/path/to/output/nameOfFile.txt",ner_result)
write_out("/path/to/index","/path/to/output/nameOfFile.txt",rake_result)
write_out("/path/to/index","/path/to/output/nameOfFile.txt",textrank_result)
write_out("/path/to/index","/path/to/output/nameOfFile.txt",bert_result)
