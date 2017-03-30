# A algorithm based on TextRank that use cortical distance measure
from cortical.client import ApiClient
from cortical.compareApi import CompareApi
from cortical.textApi import TextApi
import itertools
import math

import networkx as nx
import json

# the retina going to be used, please visit retina section 
# in api.cortical.io for more detail
retina = "en_associative"

# the cortical API key, get one from cortical.io
apiKey = "bda95f70-b90f-11e5-b6f5-5b4838bf0321"

# minimal length of a sentence
min_length = 5

# similarity measure, list :
"""
 'cosineSimilarity': 0.06177432547094736,
 'euclideanDistance': 0.9382352941176471,
 'jaccardDistance': 0.9681335356600911,
 'overlappingAll': 21,
 'overlappingLeftRight': 0.06069364161849711,
 'overlappingRightLeft': 0.06287425149700598,
 'sizeLeft': 346,
 'sizeRight': 334,
 'weightedScoring
"""
# for more information, refer to http://documentation.cortical.io/similarity_metrics.html
similarity_measure = '{0}.cosineSimilarity'

# cosine similarity for sparse fingerprint position in cortical
def cosine_similarity(position1, position2):
    it1,it2 = iter(position1),iter(position2)
    a,b = -1,-2
    similarity = 0
    
    try:
        while(True):
            if (a == b):
                similarity += 1
                a = next(it1)
            elif (a < b):
                a = next(it1)
            else:
                b = next(it2)
    except StopIteration as stop:
        None
    
    try:
        return similarity / (math.sqrt(len(position1)) * math.sqrt(len(position2)))
    except ZeroDivisionError as e:
        return 0

def summarize(text, len_sentences = 5, retina = retina, apiKey = apiKey,
              min_length = min_length, similarity_measure = similarity_measure) :
    sentences = [sentence for sentence in text.split(".") if len(sentence) >= min_length]
    
    # Make request to cortical to compare sentence by sentence to get distance
    # for graph
    
    # graph representation, to use : graph[0][1] is edge of vertex 0 to 1
    graph = nx.Graph()
    
    request_body = []
    for s in sentences:
        request_body.append({"text":s})
    
    request_body = json.dumps(request_body)
    
    client = ApiClient(apiKey=apiKey, apiServer="http://api.cortical.io/rest")
    api = TextApi(client)
    fingerprints = api.getRepresentationsForBulkText(retina, request_body)    
    
    pos_fingerprints = zip(range(0,len(sentences)),fingerprints)
    
    double_pos_fingerprints = itertools.combinations(pos_fingerprints, 2)    
    
    for (pos1,finger1),(pos2,finger2) in double_pos_fingerprints:
        graph.add_weighted_edges_from([(pos1,pos2,
                                        cosine_similarity(finger1.positions,
                                                          finger2.positions))])
        print(pos1,pos2)
    """
    request_body = []
    for s in sentences:
        for s2 in sentences:
            request_body.append([{"text":s},{"text":s2}])
    
    request_body = json.dumps(request_body)
    
    client = ApiClient(apiKey=apiKey, apiServer="http://api.cortical.io/rest")
    api = CompareApi(client)
    print("Sending to compare API")
    metrics = api.compareBulk(retina, request_body)    
    print("Receive compare API")

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            graph.add_weighted_edges_from([(i,j,metrics[i*len(sentences)+j])].cosineSimilarity)
    """
    pos_fingerprints = zip(range(0,len(sentences)),fingerprints)
        
    # Compute pagerank for all vertex in matrix, refer to https://en.wikipedia.org/wiki/PageRank
    page_rank = nx.pagerank(graph)
    
    sorted_rank = [(page_rank[key],key) for key in page_rank]
    sorted_rank.sort(reverse = True)
    
    summary_graph = nx.Graph()
    summaries = [pos for weight,pos in sorted_rank[:len_sentences]]
    
    for i in range(0,len(summaries)):
        for j in range(i+1,len(summaries)):
            summary_graph.add_weighted_edges_from([(summaries[i],summaries[j],
                                                    graph[i][j]['weight'])])
    
    gr = nx.minimum_spanning_tree(summary_graph)
    
    visited = {}
    summary = []
    for tup in list(nx.dfs_edges(gr)):
        for first in tup:
            if (visited.get(first) is None):
                summary.append(sentences[first])
                visited[first] = True
    
    return summary
    
def multi_text_summarize(texts) :
    aggregate_summarization = ""
    for text in texts:
        aggregate_summarization += summarize(text) + '.'
            
    return summarize(aggregate_summarization)
    # Another option
    """
    all_text = sum(texts)
    return summarize(all_text)
    """

if __name__ == "__main__":
    with open("magic.txt",encoding="utf8") as magic_text:
        text = magic_text.read()
        summ = summarize(text,10)
        for sentence in summ:
            print(sentence.encode('cp850', errors='replace'))