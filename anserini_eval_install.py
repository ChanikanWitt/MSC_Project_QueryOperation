# Anserini installation & trec_eval installation

%%capture
!apt-get install maven -qq
%%capture
!git clone --recurse-submodules https://github.com/castorini/anserini.git
%cd anserini
!cd eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make
!mvn clean package appassembler:assemble -DskipTests -Dmaven.javadoc.skip=true
!cd /content/anserini/tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../..
!cd /content/anserini/tools/eval && cd ndeval && make && cd ../..
#checking Anserini version: should be 0.9.5
!ls target