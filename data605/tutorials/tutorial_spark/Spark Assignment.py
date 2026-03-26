# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import json
import re
class DisplayRDD:
        def __init__(self, rdd):
                self.rdd = rdd

        def _repr_html_(self):                                  
                x = self.rdd.mapPartitionsWithIndex(lambda i, x: [(i, [y for y in x])])
                l = x.collect()
                s = "<table><tr>{}</tr><tr><td>".format("".join(["<th>Partition {}".format(str(j)) for (j, r) in l]))
                s += '</td><td valign="bottom" halignt="left">'.join(["<ul><li>{}</ul>".format("<li>".join([str(rr) for rr in r])) for (j, r) in l])
                s += "</td></table>"
                return s


# %%
## Load data into RDDs
playRDD = sc.textFile("datafiles/play.txt")
logsRDD = sc.textFile("Assignment-5-Autograder/bigdatafiles/NASA_logs_sample.txt")
amazonInputRDD = sc.textFile("datafiles/amazon-ratings.txt")
nobelRDD = sc.textFile("datafiles/prize.json")

## The following converts the amazonInputRDD into 2-tuples with integers
amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()

# A hack to avoid having to pass 'sc' around
dummyrdd = None
def setDefaultAnswer(rdd): 
    global dummyrdd
    dummyrdd = rdd
setDefaultAnswer(sc.parallelize([0]))


# %%
def task1(amazonInputRDD):
        return dummyrdd
task1_result = task1(amazonInputRDD)
for x in task1_result.takeOrdered(10):
    print(x)


# %%
def task2(amazonInputRDD):
        return dummyrdd
task2_result = task2(amazonInputRDD)
for x in task2_result.takeOrdered(10):
    print(x)


# %%
def task3(amazonInputRDD):
        return dummyrdd
task3_result = task3(amazonInputRDD)
for x in task3_result.takeOrdered(10):
    print(x)      


# %%
def task4(logsRDD):
        return dummyrdd
task4_result = task4(logsRDD)
for x in task4_result.takeOrdered(10):
    print(x)


# %%
def task5_flatmap(x):
        return []

task5_result = playRDD.flatMap(task5_flatmap).distinct()
print(task5_result.takeOrdered(100))


# %%
def task6(playRDD):
        return dummyrdd

task6_result = task6(playRDD)
for x in task6_result.takeOrdered(10):
    print(x)


# %%
def task7_flatmap(x):
        return []

task7_result = nobelRDD.map(json.loads).flatMap(task7_flatmap).distinct()
print(task7_result.takeOrdered(10))


# %%
def task8(nobelRDD):
        return dummyrdd

task8_result = task8(nobelRDD)
for x in task8_result.takeOrdered(10):
        print(x)


# %%
def task9(logsRDD, l):
        return dummyrdd
def task91(logsRDD, l):
        def extractHost(logline):
                match = re.search('^(\S+) ', logline)
                return match.group(1) if match is not None else None
        r1 = logsRDD.map(lambda s: (extractHost(s), [d in s for d in l]))
        #r2 = r1.reduceByKey(lambda x1, x2: (x1[0] or x2[0], x1[1] or x2[1]))
        r2 = r1.reduceByKey(lambda x1, x2: tuple([x1[i] or x2[i] for i in range(0, len(l))]))
        return r2.filter(lambda x: all(v for v in x[1])).map(lambda x: x[0])


def task92(logsRDD, l):
    return logsRDD.map(lambda x: ([word for word in x.split(" ") if word != ''][0], re.search(r"\d{2}/[a-zA-Z]{3}/\d{4}", x).group()))

        #return logsRDD.map(lambda x: ([word for word in x.split(" ") if word != ''][0], re.search(r"\d{2}/[a-zA-Z]{3}/\d{4}", x).group())).groupByKey().map(lambda x: x[0] if set(dict.fromkeys(x[1]))==set(l) else '').filter(lambda x: x!='').distinct()

def task93(logsRDD, l):
        def helper1(line):
                array_of_words = line.split()
                if (array_of_words[3][1: 12] in l):
                        return (array_of_words[0], (array_of_words[3][1: 12]))
                        


        def helper2(line):
                in_all = True
                for date in l:
                        if(date not in list(line[1])):
                                in_all = False
                return in_all   

        def helper3(line):
                return (line[0], list(line[1]))
                
        
                
        logs_rdd_1 = logsRDD.map(helper1).distinct()
        print(logs_rdd_1.count())
        logs_rdd_2 = logs_rdd_1.groupByKey()
        print(logs_rdd_2.count())
        logs_rdd_3 = logs_rdd_2.filter((helper2))
        print(logs_rdd_3.count())
        logs_rdd_4 = logs_rdd_3.map(lambda x: (x[0]))
        print(logs_rdd_4.count())
        return logs_rdd_4

    
task9_result = task93(logsRDD, ['02/Jul/1995', '03/Jul/1995', '04/Jul/1995', '05/Jul/1995', '06/Jul/1995'])
print(task9_result.count())
for x in task9_result.takeOrdered(10):
    print(x)


# %%
def task10(bipartiteGraphRDD):
        return dummyrdd
task10_result = task10(amazonBipartiteRDD)
print(task10_result.collect())

# %%
