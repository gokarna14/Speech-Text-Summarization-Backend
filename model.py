from sklearn.feature_extraction.text import CountVectorizer
from ntpath import join
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
# from gensim.parsing.preprocessing import remove_stopwords
# from nltk.corpus import stopwords
import string
from stopWords import stop_Words


    
def remove_stopwords(sentence):
    words = sentence.split()
    
    res = ""
    
    for word in words:
        if word not in stop_Words:
            res += word + " "
    return res

def extractandfeature(name,compression):

    lines=name.split(".")

    doc_test = []
    for i in range(len(lines)):
        doc_test.append(lines[i].split('.'))

    final_doc = []
    for i in range(len(doc_test)):
        for j in range(len(doc_test[i])):
            final_doc.append(doc_test[i][j])

    without_stopwords = []
    for i in final_doc:
        filtered_sentence = remove_stopwords(i)
        without_stopwords.append(filtered_sentence)

    without_SandP = []
    for i in without_stopwords:
        filtered_sentence = i.translate(
            str.maketrans('', '', string.punctuation))
        without_SandP.append(filtered_sentence)

    vectorizer = CountVectorizer()

    bag_of_words = vectorizer.fit_transform(without_SandP)
    bag_of_words.todense()
    svd = TruncatedSVD(n_components=1)
    lsa = svd.fit_transform(bag_of_words)
    topic_encoded_df = pd.DataFrame(lsa, columns=["topic1"])
    topic_encoded_df["without_stopwords"] = without_stopwords
    # topic_encoded_df[["without_stopwords", "topic1"]]
    dictionary = vectorizer.get_feature_names_out()
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
        words_after_compression.append(index_list[0])
    elif compression <= 0.66 and compression > 0.33:
        words_after_compression.append(index_list[0])
        words_after_compression.append(index_list[1])
    else:
        words_after_compression.extend(index_list)


    final_conclusion = []
    for i in range(len(final_doc)):
        for j in range(len(words_after_compression)):
            if words_after_compression[j] in final_doc[i]:
                final_conclusion.append(final_doc[i])

    list_final = list(set(final_conclusion))

    summ_final = '.'.join(list_final) + "."
    significant_final = ' '.join(index_list)

    res = {
        "summary": summ_final,
        "significant_words": significant_final
    }

    return res



# sample_str = """The World Soil Day is being observed today globally as well as in Nepal with the objective of raising public awareness on the significance of healthy soil and for the sustainable management of the soil fertility.The United Nations General Assembly had in December 2013 declared December 5, 2014 as the World Soil Day and it was formally marked throughout the world since then. Nepal has been observing the Day since 2015. The theme of the World Soil Day this year is 'Soils: where food begins.' Soil is at the heart of all agricultural activities, food security, nutrition security and climate conservation.
# The World Soil Day programme reiterates the importance of soil for mankind and the crucial need for its conservation and proper management while at the same time increasing its fertility, the Department of Agriculture said.Director General of the Department, Dr Rewati Raman Poudel said that the debate about food and nutritional security, sustainable agriculture development, conservation of bio-diversity and organic agriculture will have no meaning without the conservation, promotion and proper management of soil.
# The soil fertility is deteriorating throughout the world including in Nepal in the recent years with the declining physical, chemical and biological features of the soil. Therefore, this problem of declining soil fertility has been taken as the common global problem.
# Poudel said the World Soil Day is being marked with the main goal of raising extensive public awareness to tackle this growing problem of loss in soil fertility.
# The World Soil Day is being celebrated at the national level today in Nepal amidst various programmes under the aegis of the Department, Central Agricultural Laboratory, the National Soil Science Research Centre (NARC), Food and Nutrition Security Improvement Project, Rural Enterprises and Economic Development Project, United Nations, Food and Agriculture Organization and the Nepalese Society of Soil Science.
# # The UN has said that over the last 70 years, the level of vitamins and nutrients in food has drastically decreased, and it is estimated that 2 billion people worldwide suffer from lack of micronutrients, known as hidden hunger because it is difficult to detect.
# # Soil degradation induces some soils to be nutrient depleted losing their capacity to support crops, while others have such a high nutrient concentration that represent a toxic environment to plants and animals, pollutes the environment and cause climate change.
# # World Soil Day 2022 and its campaign "Soils: Where food begins" aims to raise awareness of the importance of maintaining healthy ecosystems and human well-being by addressing the growing challenges in soil management, increasing soil awareness and encouraging societies to improve soil health.
# """

# out_final=extractandfeature(sample_str,0.2)


# print(out_final)