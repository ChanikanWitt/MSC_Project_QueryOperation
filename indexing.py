# Indexing using Anserini and Calculating baseline

print("========== Indexing start ==========")
!target/appassembler/bin/IndexCollection -collection WashingtonPostCollection -input path_data \
	 -index path_out -generator WashingtonPostGenerator -threads 9 \
	 -storePositions -storeDocvectors -storeRaw -storeContents 
print("========== Indexing completed ==========")
print("========== Retrieval start ==========")
#Using BM25
!target/appassembler/bin/SearchCollection -index indexes/lucene-index.core18.pos+docvectors+raw \
 -topicreader BackgroundLinking -topics src/main/resources/topics-and-qrels/topics.backgroundlinking19.txt \
 -backgroundlinking -backgroundlinking.k 100 -bm25 -hits 100 -output run.backgroundlinking19.bm25.topics.backgroundlinking19.txt &
#Using BM25+RM3
!target/appassembler/bin/SearchCollection -index indexes/lucene-index.core18.pos+docvectors+raw \
 -topicreader BackgroundLinking -topics src/main/resources/topics-and-qrels/topics.backgroundlinking19.txt \
 -backgroundlinking -backgroundlinking.k 100 -bm25 -rm3 -hits 100 -output run.backgroundlinking19.bm25+rm3.topics.backgroundlinking19.txt &
#Using QL+RM3
!target/appassembler/bin/SearchCollection -index indexes/lucene-index.core18.pos+docvectors+raw \
 -topicreader BackgroundLinking -topics src/main/resources/topics-and-qrels/topics.backgroundlinking19.txt \
 -backgroundlinking -backgroundlinking.k 100 -qld -rm3 -hits 100 -output run.backgroundlinking19.qld+rm3.topics.backgroundlinking19.txt &
print("========== Retrieval completed ==========")
print("========== Evaluation start ==========")
!eval/trec_eval.9.0.4/trec_eval -c -M1000 -m ndcg_cut.5 -c -M1000 -m map src/main/resources/topics-and-qrels/qrels.backgroundlinking19.txt run.backgroundlinking19.bm25.topics.backgroundlinking19.txt
!eval/trec_eval.9.0.4/trec_eval -c -M1000 -m ndcg_cut.5 -c -M1000 -m map src/main/resources/topics-and-qrels/qrels.backgroundlinking19.txt run.backgroundlinking19.bm25+rm3.topics.backgroundlinking19.txt
!eval/trec_eval.9.0.4/trec_eval -c -M1000 -m ndcg_cut.5 -c -M1000 -m map src/main/resources/topics-and-qrels/qrels.backgroundlinking19.txt run.backgroundlinking19.qld+rm3.topics.backgroundlinking19.txt
print("========== Retrieval completed ==========")