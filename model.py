from sklearn.feature_extraction.text import CountVectorizer
from ntpath import join
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from gensim.parsing.preprocessing import remove_stopwords
import string

from transformers import pipeline
summarizer = pipeline('summarization')

    
def abs_summary(article):
    l = len(list(article.split()))
    abs_summ = summarizer(article,max_length=l,min_length=int(l/2),do_sample=False)[0]['summary_text']
    x = abs_summ.split(".")
    abs_final = []
    for i in x:
        if (len(i.split(" ")) > 8):
            abs_final.append(i)

    abs_Sumfinal = '.'.join(abs_final) + "."

    return abs_Sumfinal


def extractandfeature(name,compression):
    name = name.replace("\n"," ")
    name = name.replace("\r"," ")

    lines=name.split(".")
    str_lower = name.lower()

    doc_test = []
    for i in range(len(lines)):
        doc_test.append(lines[i].split('.'))

    final_doc = []
    for i in range(len(doc_test)):
        for j in range(len(doc_test[i])):
            final_doc.append(doc_test[i][j])

    lines = str_lower.split(".")
    doc_test = []
    for i in range(len(lines)):
        doc_test.append(lines[i].split('.'))

    final_doc1 = []
    for i in range(len(doc_test)):
        for j in range(len(doc_test[i])):
            final_doc1.append(doc_test[i][j])

    without_P = []
    for i in final_doc1:
        filtered_sentence = i.translate(
            str.maketrans('', '', string.punctuation))
        without_P.append(filtered_sentence)

    without_stopwords = []
    for i in without_P:
        filtered_sentence = remove_stopwords(i)
        without_stopwords.append(filtered_sentence)

    vectorizer = CountVectorizer()

    bag_of_words = vectorizer.fit_transform(without_stopwords)
    bag_of_words.todense()
    svd = TruncatedSVD(n_components=1)
    lsa = svd.fit_transform(bag_of_words)
    topic_encoded_df = pd.DataFrame(lsa, columns=["topic1"])
    topic_encoded_df["without_stopwords"] = without_stopwords
    # topic_encoded_df[["without_stopwords", "topic1"]]
    dictionary = vectorizer.get_feature_names()
    # print(dictionary)
    encoding_matrix = pd.DataFrame(svd.components_, index=[
                                   "topic1"], columns=dictionary).T
    encoding_matrix['abs_topic1'] = np.abs(encoding_matrix)
    encoding_matrix.sort_values('abs_topic1', ascending=False)
    final_matrix = encoding_matrix.sort_values('abs_topic1', ascending=False)
    # sentence1 = final_matrix[final_matrix["abs_topic1"] >= 0.2]
    sentence1 = final_matrix.head(4)
    index_list = list(sentence1.index.values)

    words_after_compression = []
    if compression <= 0.33:
        words_after_compression.append(index_list[2])
    elif compression <= 0.66 and compression > 0.33:
        words_after_compression.append(index_list[2])
        words_after_compression.append(index_list[3])
    else:
        words_after_compression.extend(index_list)


    final_conclusion = []
    for i in range(len(final_doc)):
        for j in range(len(words_after_compression)):
            if words_after_compression[j] in final_doc[i]:
                final_conclusion.append(final_doc[i])

    list_final = list(set(final_conclusion))

    summ_final = '.'.join(list_final) + "."
    # significant_final = ' '.join(index_list)

    res = {
        "summary": summ_final,
        "significant_words": index_list
    }

    words_after_compression = []
    words_after_compression.extend(index_list)
    final_conclusion = []
    for i in range(len(final_doc)):
        for j in range(len(words_after_compression)):
            if words_after_compression[j] in final_doc[i]:
                final_conclusion.append(final_doc[i])

    list_final = list(set(final_conclusion))

    summ_final = '.'.join(list_final) + "."


    res["abs_summ"] = summ_final

    return res

def get_abs(text):
    return {"abs_summ" : abs_summary(text)}



# sample_str = """"Hey guys,

# I want to share with you all the story of my day. It may not be the most exciting thing you've ever heard, but I think it's a reminder that sometimes it's the little things that make life special.

# I woke up early this morning, feeling pretty groggy. I stumbled out of bed and made my way to the kitchen to make some coffee. Honestly, that first sip of coffee was the best thing that happened to me all day!

# After waking up a bit, I got dressed and headed to work. I spent most of the day in meetings and answering emails, but I managed to squeeze in some actual work too. It wasn't the most exciting day at the office, but I always feel good when I'm productive.

# At lunchtime, I met up with some coworkers and we grabbed some food at a nearby deli. We chatted and laughed and I always love taking a break to hang out with my work buddies.

# After work, I went to the gym and had a great workout. I always feel energized and refreshed after exercise, and it's one of the highlights of my day.

# When I got home, I had dinner with my family and we chatted about our day. It was nice to catch up and spend some quality time together.

# After dinner, I settled in on the couch with my dog and watched some TV. It was a nice way to unwind and relax after a busy day.

# So that's the story of my day. It may not be the most thrilling thing in the world, but I always try to find joy in the little things. And I think that's what makes life really special. Thanks for listening!"""

# out_final=extractandfeature(sample_str,0.2)


# print(out_final)