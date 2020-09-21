#!pip install pyserini==0.9.4.0
#!pip install rake-nltk
#!pip install pytextrank
#!pip install bert-extractive-summarizer
#!pip install neuralcoref
#!pip install transformers==2.2.2
!python -c "import nltk; nltk.download('stopwords')"
from pyserini.search import SimpleSearcher
from pyserini import analysis, index
from rake_nltk import Rake
import pytextrank
from summarizer import Summarizer
import spacy
#path to index document (output from Anserini indexing)
path_index = "/content/indexes/lucene-index.core18.pos+docvectors+raw/"
searcher = SimpleSearcher(path_index)
index_utils = index.IndexReader(path_index)

nlp = spacy.load('en_core_web_sm')

ner_out = []
rake_out = []
textrank_out = []
bert_out = []
#add textrank into spacy pipeline
textrank_pipe = pytextrank.TextRank()
textrank_pipe.load_stopwords(path="stop.json")
nlp.add_pipe(textrank_pipe.PipelineComponent, name="textrank", last=True)

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

def ner(ner_out):
  #loop topic queries
  for i in range(len(docid)):
    doc = nlp(index_utils.doc_contents(docid[i]))
    print("=== %d ===" %i)
    ner = []
    ner_unique = []
    # find name entity recognization(NER) of docid
    for ent in doc.ents:
      #print(ent.text)
      #append every entity
      ner.append(ent.text)
    # delete redundancy term
    str_ner = " "  
    for x in ner:
      if x not in ner_unique:
        ner_unique.append(x)
    # convert to string
    str_ner = str_ner.join(ner_unique) 
    print(str_ner)
    # save in list -> 60 docid
    ner_out.append(str_ner)
    return ner_out

def rake_extract(rake_out):
  for i in range(len(docid)):
    doc = index_utils.doc_contents(docid[i])
    print("=== %d ===" %i)
    #find keyphrase extraction
    #Uses stopwords for english from NLTK, and all puntuation characters.
    r = Rake(min_length=2, max_length=10) 
    r.extract_keywords_from_text(doc)
    str_rake = " "
    # convert to string
    str_rake = str_rake.join(r.get_ranked_phrases()[:60]) 
    print(str_rake)
    # save in list -> 60 docid
    rake_out.append(str_rake)
    return rake_out

def textrank_extract(textrank_out):
  for i in range(len(docid)): 
    print("=== %d ===" %i)
    tr_append = []
    doc = nlp(index_utils.doc_contents(docid[i]))
    #find keyphrase extraction
    for x in doc._.phrases:
      tr_append.append(x.text)
    # delete redundancy term
    str_tr = " "  
    # convert to string
    str_tr = str_tr.join(ner4[:90]) 
    print(str_tr)
    # save in list -> 60 docid
    textrank_out.append(str_tr)
    return textrank_out

def bert_sum(bert_out):
  for i in range(len(docid)):
    doc = index_utils.doc_contents(docid[i])
    print("=== %d ===" %i)
    model = Summarizer()
    result = model(doc, min_length=60, ratio=0.2)
    str_bert = " "
    str_bert = str_bert.join(result)
    print(str_bert)
    # save in list -> 60 docid
    bert_out.append(str_bert)
    return bert_out

#Using all of functions
ner_result = ner(ner_out)
rake_result = rake_extract(rake_out)
textrank_result = textrank_extract(textrank_out)
bert_result = bert_sum(bert_out) 

#Writing all query operations files
write_out("/path/to/index","/path/to/output/nameOfFile1.txt",ner_result)
write_out("/path/to/index","/path/to/output/nameOfFile2.txt",rake_result)
write_out("/path/to/index","/path/to/output/nameOfFile3.txt",textrank_result)
write_out("/path/to/index","/path/to/output/nameOfFile4.txt",bert_result)